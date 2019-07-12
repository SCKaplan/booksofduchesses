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

            owners_search = request.POST.get('owner', '')
            owners_to_map = Owner.objects.filter(name__icontains=owners_search)
            t = []
            b = []
            for owner in owners_to_map:
                t.append(owner.owner_location.all().order_by('date_at_location'))
            for set in t:
                for item in set:
                    b.append(item)

            books_to_map = Book.objects.filter(shelfmark__icontains=shelfmark)
            z = []
            a = []
            for book in books_to_map:
                z.append(book.book_location.all().order_by('date'))
            for locs in z:
                for loc in locs:
                    a.append(loc)

            if len(display) == 0 or display[0] == 'owners':
                # If we only want to display owners
                a = []
            if len(display) == 1 and display[0] == 'books':
                # If we only want to display books
                b = []

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
    texts = Text.objects.filter(book=book)
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
    # owner_id should be the name of an owner if we did this right
    owner = Owner.objects.get(name=owner_id)
    # We need Owner Name, Motto, Title, Locations, Library
    location = owner.owner_location.all().order_by('date_at_location')
    books = owner.book_date.all().order_by('book_owned__shelfmark')
    relatives = owner.relation.all()
   # places = []
  #  for place in location:
   #     places.append(place.the_place)
    return render(request, 'owners.html', {'places': location, 'relatives': relatives, 'books':books, 'owner':owner, 'locations':location})

def texts(request, text_id):
    text = Text.objects.get(title=text_id)
    books = text.book.all()
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
    books = Book.objects.all()
    for book in books:
        dateinfo = DateOwned.objects.filter(book_owned=book)
        places = []
        for date in dateinfo:
            # In case of random unlinked data entries
            try:
                ownergeo = Owner.objects.get(book_date=date)
                dateRange = date.date_range()
            except:
                continue
            # Now we have to compare this date range to one generated by the owner locations
            locations = ownergeo.owner_location.all()
            for location in locations:
                ownerRange = location.date_range()
                if dateRange[1] >= ownerRange[0] and dateRange[0] <= ownerRange[1]:
                    # Add the owners location
                    places.append((location, ownergeo))
        # create an book location object for each place
        for tuple in places:
            place = tuple[0]
            b = BookLocation(geom=place.geom, book_location=place.the_place, date=place.date_at_location, book_shelfmark=book, owner_at_time=tuple[1])
            b.save()
            book.book_location.add(b)
            book.save()
    return HttpResponse('Book Locations loaded')
