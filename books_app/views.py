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

            # Search queries for books, authors and owners
            query = request.POST.get('search', '')

            author_result = Author.objects.filter(name__icontains=query)

            owners_result = Owner.objects.filter(name__icontains=query)

            locations = Location.objects.filter(name__icontains=query)

            author = request.POST.get('author', '')
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')

            owners_search = request.POST.get('owner', '')
            owners_to_map = Owner.objects.filter(name__icontains=owners_search)
            t = []
            b = []
            for owner in owners_to_map:
                t.append(owner.owner_location.all().order_by('date_at_location'))
            for set in t:
                for item in set:
                    b.append(item)

            genre = request.POST.get('genre', '')
            text = request.POST.get('text', '')
            shelfmark = request.POST.get('shelfmark', '')

            return render(request, 'index.html',
                          #{'books': books_result, 'locations': locations, 'search_form': search_form, 'authors': author_result, 'owners':owner_result}
                          {'locations': locations, 'search_form': search_form, 'authors': author_result, 'owners':b, }
                        )

    # if a GET (or any other method) we'll create a blank form
    else:
        books = Book.objects.all()
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

def books(request):
    return render(request,'books.html')

def owners(request, owner_id):
    # owner_id should be the name of an owner if we did this right
    owner = Owner.objects.get(name__contains=owner_id)
    # We need Owner Name, Motto, Title, Locations, Library
    location = owner.owner_location.all().order_by('date_at_location')
    books = owner.book_date.all().order_by('book_owned__shelfmark')
    relatives = owner.relation.all()
   # places = []
  #  for place in location:
   #     places.append(place.the_place)
    return render(request, 'owners.html', {'places': location, 'relaitve': relatives, 'books':books, 'owner':owner, 'locations':location})

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
   # csvinfo = open('books_app/csvs/bibs2.csv', 'r')
    #for line in csvinfo:
     #   line  = line.replace('\n', '')
      #  line = line.split(',')
        # We get a bib reference and a bunch of ! seperated books
       # bib = line[0]
        #bib = bib.replace('!', ',')
      #  bib = bib.rstrip()
       # bibToAdd = Bibliography.objects.filter(author_date__contains=bib)

#        books = line[1]
 #       books = books.split('!')
        # probably need to filter here for \n
  #      for book in books:
   #         book = book.lstrip()
    #        if len(book) != 0:
     #           bookToEdit = Book.objects.filter(shelfmark__contains=book)
      #      if len(bookToEdit) != 0 and len(bibToAdd) != 0:
       #         bookToEdit[0].bibliography.add(bibToAdd[0])
        #        bookToEdit[0].save()
         #   else:
          #      print("This bibliography is not in the database")

    return HttpResponse('Thanks')
