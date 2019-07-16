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
            author_result = Author.objects.filter(name__icontains=query)
            owners_result = Owner.objects.filter(name__icontains=query)
            locations = Location.objects.filter(name__icontains=query)

            # Owners search field
            owners_search = request.POST.get('owner', '')
            owners_to_map = Owner.objects.filter(name__icontains=owners_search)
            t = []
            b = []
            for owner in owners_to_map:
                t.append(owner.owner_location.all().order_by('date_at_location'))
            for set in t:
                for item in set:
                    b.append(item)

            # Book shelfmark search field
            books_to_map = Book.objects.filter(shelfmark__icontains=shelfmark)
            z = []
            a = []
            for book in books_to_map:
                z.append(book.book_location.all().order_by('date'))
            for locs in z:
                for loc in locs:
                    a.append(loc)

            # Text search field goes here

            # Display options
            if len(display) == 0 or display[0] == 'owners':
                # If we only want to display owners
                a = []
            if len(display) == 1 and display[0] == 'books':
                # If we only want to display books
                b = []

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

            # Date range filtering
            for item in a:
                dateRange = item.date_range()
                # decide to display each owner or not
                if dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]:
                    a.remove(item)
            for thing in b:
                dateRange = thing.date_range()
                # decide to display each owner or not
                if dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]:
                    b.remove(thing)

            return render(request, 'index.html',
                          #{'books': books_result, 'locations': locations, 'search_form': search_form, 'authors': author_result, 'owners':owner_result}
                          {'locations': locations, 'search_form': search_form, 'authors': author_result, 'owners':b, 'display':display, 'books':a}
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
            t.append(owner.owner_location.all())
        for set in t:
            for item in set:
                b.append(item.the_place)
        search_form = SearchForm()

        return render(request, 'index.html',{'books':books, 'locations':locations, 'search_form': search_form, 'authors': authors, 'owners':b})

def books(request, book_id):
    book = Book.objects.get(shelfmark=book_id)
    texts = book.text.all()
    owners = DateOwned.objects.filter(book_owned=book).order_by('dateowned')
    bibs = book.bibliography.all()
    l = []
    for owner in owners:
        try:
            # In case some misc dateowned objects appear- if everything has a link and we clean up this isn't necessary
            l.append((Owner.objects.get(book_date=owner), owner.dateowned))
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
    books = owner.book_date.all().order_by('book_owned__shelfmark')
    relatives = owner.relation.all()
    #places = []
    #for place in location:
        #places.append(place.the_place)
    return render(request, 'owners.html', {'places': location, 'relatives': relatives, 'books':books, 'owner':owner, 'locations':location})

def texts(request, text_id):
    text = Text.objects.get(title=text_id)
    books = Book.objects.filter(text=text)
    languages = text.language.all()
    if len(languages) == 0:
        languages = None
    tags = text.tags.all()
    return render(request, 'texts.html', {'text': text, 'books': books, 'languages': languages, 'tags': tags})

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
#	textinfo = open('books_app/csvs/texttransfer.csv', 'r')
#	for line in textinfo:
#		line = line.split(',')
#		book = Book.objects.filter(shelfmark=line[0])
#		texts = line[1]
#		texts = texts.split('!')
#		if len(book) != 0:
#			book = book[0]
#			for text in texts:
#				text = text.lstrip()
#				text = text.replace('"', '')
#				toAdd = Text.objects.filter(title__contains=text)
#				if len(toAdd) != 0:
#					book.text.add(toAdd[0])
#			book.save()
#	textinfo.close()
	return HttpResponse('Success')
