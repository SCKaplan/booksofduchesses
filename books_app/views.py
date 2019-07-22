from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from books_app.models import *
from books_app.forms import SearchForm


# Create your views here.

def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        search_form = SearchForm(request.POST)
        # check whether it's valid:
        if search_form.is_valid():
            display = request.POST.getlist('display')
            query = request.POST.get('search', '')
            author = request.POST.get('author', '')
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            genre = request.POST.get('genre', '')
            text = request.POST.get('text', '')
            shelfmark = request.POST.get('shelfmark', '')

            # Search queries for books, authors and owners
            author_result = Author.objects.filter(name__icontains=author)
            owners_result = Owner.objects.filter(name__icontains=query)
            locations = Location.objects.filter(name__icontains=query)

            # Owners search field
            owners_search = request.POST.get('owner', '')
            owners_objs = Owner.objects.filter(name__icontains=owners_search)
            t = []
            owner_to_filter = []
            for owner in owners_objs:
                t.append(owner.owner_location.all().order_by('date_at_location'))
            for queryset in t:
                for item in queryset:
                    owner_to_filter.append(item)

            # Book shelfmark search field
            books_objs = Book.objects.filter(shelfmark__icontains=shelfmark)
	    # Author Search Field
            texts_from_author = []
            books_from_author = []
            for auth in author_result:
                text = Text.objects.filter(author=auth)
                for element in text:
                    texts_from_author.append(element)
            for text_obj in texts_from_author:
                book = Book.objects.filter(text=text_obj)
                for b in book:
                    books_from_author.append(b)
            if len(author) != 0:
                books_objs = set(books_from_author) & set(books_objs)

            z = []
            books_to_filter = []
            for book in books_objs:
                z.append(book.book_location.all().order_by('date'))
            for locs in z:
                for loc in locs:
                    books_to_filter.append(loc)

            # Display options
            if len(display) == 0 or display[0] == 'owners':
                # If we only want to display owners
                books_to_filter = []
            if len(display) == 1 and display[0] == 'books':
                # If we only want to display books
                owner_to_filter = []

            # Date range search field
            searchRange = []
            if len(start_date) != 4:
                searchRange.append(datetime.datetime(1350, 1, 1))
            else:
                searchRange.append(datetime.datetime(int(start_date), 1, 1))
            if len(end_date) != 4:
                searchRange.append(datetime.datetime(1500, 1, 1))
            else:
                searchRange.append(datetime.datetime(int(end_date), 1, 1))
            # Date range filtering for books
            books_final = []
            for date in books_to_filter:
                dateRange = date.date_range()
                # decide to display each book or not
                if not(dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    books_final.append(date)
	    # For owners
            owners_final = []
            for owner_date in owner_to_filter:
                dateRange = owner_date.date_range()
                # decide to display each owner or not
                if not(dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    owners_final.append(owner_date)

            return render(request, 'index.html',
                          #{'books': books_result, 'locations': locations, 'search_form': search_form, 'authors': author_result, 'owners':owner_result}
                          {'locations': locations, 'search_form': search_form, 'authors': author_result, 'owners': owners_final, 'display':display, 'books': books_final}
                        )

    # if a GET (or any other method) we'll create a blank form
    else:
        books = []
        locations = Location.objects.all()
        authors = Author.objects.all()
        owners = Owner.objects.filter(gender="Female")
        t = []
        b = []
        for owner in owners:
           # if len(owner.owner_location.all()) != 0:
            toAdd = owner.owner_location.all()
            for item in toAdd:
                t.append(item)
     # for set in t:
        #    for item in set:
         #       b.append(item.the_place)
        search_form = SearchForm()

        return render(request, 'index.html',{'books':books, 'locations':locations, 'search_form': search_form, 'authors': authors, 'owners':t})

def books(request, book_id):
    book = Book.objects.get(shelfmark=book_id)
    texts = book.text.all()
    owners = DateOwned.objects.filter(book_owned=book).order_by('dateowned')
    bibs = book.bibliography.all()
    l = []
    for owner in owners:
        try:
            # In case some misc dateowned objects appear- if everything has a link and we clean up this isn't necessary
            l.append(owner)
        except:
            pass
    # Geo data for template
    places = BookLocation.objects.filter(book_shelfmark=book)
    return render(request,'books.html', {'book': book, 'owners': l, 'texts': texts, 'bibs': bibs, 'places': places})

def owners(request, owner_id):
    # owner_id should be the name of an owner
    # We need Owner Name, Motto, Title, Locations, Library
    owner = Owner.objects.get(name=owner_id)
    location = owner.owner_location.all().order_by('date_at_location')
    books = DateOwned.objects.filter(owner=owner).order_by('book_owned__shelfmark')
    relatives = owner.relation.all()
    return render(request, 'owners.html', {'places': location, 'relatives': relatives, 'books':books, 'owner':owner, 'locations':location})

def texts(request, text_id):
    text = Text.objects.get(title=text_id)
    books = Book.objects.filter(text=text)
    languages = text.language.all()
    if len(languages) == 0:
        languages = None
    tags = text.tags.all()
    places = []
    dates = []
    for book in books:
        locations = book.book_location.all()
        for location in locations:
            places.append(location)
        toAdd = book.owner_info.all()
        for date in toAdd:
            dates.append(date)
    return render(request, 'texts.html', {'text': text, 'books': books, 'languages': languages, 'tags': tags, 'places': places, 'dates' : dates})

def loadup(request):
    # if run accidentally, delete all texts and rerun
#    textinfo = open('books_app/csvs/texts14.csv', 'r')
 #   # texts = Text.objects.all()
  #  # textsIndex = 0
#    for line in textinfo:
 #       line = line.split(',')
  #      toEdit = Text.objects.create()
        # Text name, name_eng, author,translator, books,arlima,feminae,me comp,teams,tags,ihrt order in csv
        # name, name_eng, arlima are all charfields
  #      toEdit.title = line[0]
#        toEdit.name_eng = line[1]
#        toEdit.arlima_link = line[5]
#        toEdit.me_compendium_link = line[7]
 #       toEdit.ihrt_link = line[10]
        # Author is a Foreign Key so make an object
 #       author = Author.objects.filter(name__contains = line[2])
 #       if len(author) != 0 and len(author) < 3:
 #           toEdit.author = author[0]
        # Tags Many to Many Fields
 #       allTags = line[9] #[:-1]
  #      allTags = allTags.split('!')
  #      for tag in allTags:
  #          tag = tag.lstrip()
 #           if len(tag) != 0:
  #              toAdd = Tag.objects.filter(tag__contains=tag)
   #             if len(toAdd) != 0:
    #                toEdit.tags.add(toAdd[0])
        #toEdit.save()
 #      # Books Many to Many Field
     #   allBooks = line[4]
      #  allBooks = allBooks.split('!')
       # for book in allBooks:
        #    book = book.lstrip()
         #   if len(book) != 0:
          #      toAdd = Book.objects.filter(shelfmark__contains=book)
           #     # So that we don't break it, for now
            #    if len(toAdd) != 0:
              #      toEdit.book.add(toAdd[0])
             #   else:
                   # print("This is a book that is not yet loaded into the db")
       # toEdit.save()

        # textsIndex += 1
    #textinfo.close()
    return HttpResponse('Thanks')

def bibload(request):
    owners = Owner.objects.all()
    books = Book.objects.all()
    for book in books:
            dates = DateOwned.objects.filter(book_owned=book)
            for date in dates:
                book.owner_info.add(date)
            book.save()
    return HttpResponse('Success')
