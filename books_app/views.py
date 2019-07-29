from dal import autocomplete
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from books_app.models import *
from books_app.forms import SearchForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        # create a form instance
        search_form = SearchForm(request.POST)
        # check whether it's valid:
        if search_form.is_valid():
            # Get all the data from the search form
            display = request.POST.getlist('display')
            query = request.POST.get('search', '')
            author = request.POST.get('author', '')
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            tag = request.POST.get('tag', '')
            text = request.POST.get('text', '')
            shelfmark = request.POST.get('shelfmark', '')
            owners_search = request.POST.get('owner', '')

            # Book shelfmark search field- we get all the books from here and narrow the list down
            # with the other search fields
            books_objs = Book.objects.filter(shelfmark__icontains=shelfmark)

	        # Author Search Field- get all the books that contain a text by the searched author
            author_result = Author.objects.filter(name__icontains=author)
            if len(author_result) != 0:
                texts_from_author = []
                books_from_author = []
                # Create a list of texts with author
                for auth in author_result:
                    text_query = Text.objects.filter(author=auth)
                    for element in text_query:
                        texts_from_author.append(element)
                # Get all the books from texts
                for text_obj in texts_from_author:
                    book = Book.objects.filter(text=text_obj)
                    for b in book:
                        books_from_author.append(b)
                # Get the duplicate elements from the books searched frm shelfmark and from author
                books_objs = set(books_from_author) & set(books_objs)

            # Text Search Field- same process as author
            texts_from_text = Text.objects.filter(title__icontains=text)
            if len(texts_from_text) != 0:
                books_from_text = []
                for item in texts_from_text:
                    book = Book.objects.filter(text=item)
                    for c in book:
                        books_from_text.append(c)
                books_objs = set(books_from_text) & set(books_objs)

            # Tag Search Field- same process as author, added complication of tags being ManyToManyField
            if len(tag_result) != 0:
                # ^^ Prevents us from doing a lot useless work if search field is blank
                texts_from_tag = []
                books_from_tag = []
                tag_result = Tag.objects.filter(tag__icontains=tag)
                all_texts = Text.objects.all()
                for tag_obj in tag_result:
                    for a in all_texts:
                        texttags = a.tags.filter(tag=tag_obj)
                        if len(texttags) != 0:
                             texts_from_tag.append(a)
                for text_obj_tag in texts_from_tag:
                    book = Book.objects.filter(text=text_obj_tag)
                    for c in book:
                        books_from_tag.append(c)
                books_objs = set(books_from_tag) & set(books_objs)
            else:
                # Will add to the list of texts we return as a list of search results
                texts_from_tag = Text.objects.all()

            # To filter out by dates we need to get each BookLocation object, which has a date_range() attached
            z = []
            books_to_filter = []
            for book in books_objs:
                z.append(book.book_location.all().order_by('date'))
            for locs in z:
                for loc in locs:
                    # List of Book Locations to filter
                    books_to_filter.append(loc)

            owners_objs = Owner.objects.filter(name__icontains=owners_search)
            # Owners from book searches- We also have to display owners on the map if they owned a book
            # which came up from another search field
            owners_from_books = []
            if len(text) != 0 or len(author) != 0 or len(tag) != 0:
                # If another search field was filled in
                for book_obj in books_objs:
                    # Get the dates the book was owned
                    date_for_owner = DateOwned.objects.filter(book_owned=book_obj)
                    for owner_date in date_for_owner:
                        # Create a list of the owners who owned the books from the searche fields
                        owners_from_books.append(owner_date.book_owner)
                # Get the duplicates from the owner search field and all the other fields
                owners_objs = set(owners_from_books) & set(owners_objs)

            # Locations for each owner- same process as books
            t = []
            owner_to_filter = []
            for owner in owners_objs:
                t.append(owner.owner_location.all().order_by('date_at_location'))
            for queryset in t:
                for item in queryset:
                    owner_to_filter.append(item)

            # Display options- default display is only owners per request of profs.
            if len(display) == 0 or (display[0] == 'owners' and len(display) != 2):
                # If we only want to display owners
                books_to_filter = []
            if len(display) == 1 and display[0] == 'books':
                # If we only want to display books
                owner_to_filter = []

            # Date range search field
            searchRange = []
            # At the moment forces the search to be a year, this filtering could be improved
            if len(start_date) != 4:
                # If we don't get a valid year we max out the range
                searchRange.append(datetime.datetime(1350, 1, 1))
            else:
                searchRange.append(datetime.datetime(int(start_date), 1, 1))
            if len(end_date) != 4:
                searchRange.append(datetime.datetime(1500, 1, 1))
            else:
                searchRange.append(datetime.datetime(int(end_date), 1, 1))

            # Date range filtering for books
            books_final = []
            # Filter all the book locations based on their date range
            for date in books_to_filter:
                dateRange = date.date_range()
                # decide to display each book or not- the ranges must have overlap to display
                if not(dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    books_final.append(date)

	        # For owners
            owners_final = []
            for owner_date in owner_to_filter:
                dateRange = owner_date.date_range()
                # decide to display each owner or not- the ranges must have overlap to display
                if not(dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    owners_final.append(owner_date)

            # Lists to display search results below the map
            owners_search = []
            for owner_location in owners_final:
                 # Get the owners associated with each pin
                 toAppend = Owner.objects.get(owner_location=owner_location)
                 owners_search.append(toAppend)
            owners_search = list(set(owners_search))

            books_search = []
            for book_location in books_final:
                 toAdd = Book.objects.get(book_location=book_location)
                 books_search.append(toAdd)
            books_search = list(set(books_search))

            # For a search summary "your search returned (owner_len) owners..."
            owner_len = len(owners_search)
            book_len = len(books_search)
            texts_search = set(texts_from_text) & set(texts_from_tag) & set(texts_from_author)
            text_len = len(texts_search)

            # owners_final and books_final have PointFields associated with them and therefore can be mapped
            # Popups are determined by Leaflet and the models- this just decides which ones to display
            return render(request, 'index.html',{'books_search': books_search, 'owners_search': owners_search, 'search_form': search_form, 'owners': owners_final, 'display':display, 'books': books_final, 'book_len': book_len, 'owner_len': owner_len, 'text_len': text_len, 'texts_search': texts_search,})

    # if a GET (or any other method) we'll create a blank form and display all female owners
    else:
        books = []
        owners = Owner.objects.filter(gender="Female")
        owners_default = []
        # For every female owner add her known PointField locations
        for owner in owners:
            toAdd = owner.owner_location.all()
            for item in toAdd:
                owners_default.append(item)
        search_form = SearchForm()

        return render(request, 'index.html',{'books':books, 'locations':locations, 'search_form': search_form, 'authors': authors, 'owners': owners_default})

def books(request, book_id):
    # book_id comes from the url- is a book's shelfmark
    # Get all the data we need on a book and send to template
    book = Book.objects.get(shelfmark=book_id)
    texts = book.text.all()
    bibs = book.bibliography.all()
    # Geo data for the template map
    places = BookLocation.objects.filter(book_shelfmark=book)
    illuminators = book.illuminators.all()
    scribes = book.scribes.all()
    # For owners we query DateOwned objects because they contain dates which we need to be on template
    owners_date = DateOwned.objects.filter(book_owned=book).order_by('dateowned')
    owner_geo = []
    for owner in owners_date:
        try:
            # In case some misc dateowned objects appear- if everything has a link and we clean up this isn't necessary
            owner_geo.append(owner)
        except:
            pass
    return render(request,'books.html', {'book':book, 'owners':owner_geo, 'texts': texts, 'bibs': bibs, 'places':places, 'iluminators': illuminators, 'scribes': scribes})

def owners(request, owner_id):
    # owner_id is the name of an owner
    # Get all owner data for the template
    owner = Owner.objects.get(name=owner_id)
    location = owner.owner_location.all().order_by('date_at_location')
    books = DateOwned.objects.filter(owner=owner).order_by('book_owned__shelfmark')
    relatives = owner.relation.all()
    return render(request, 'owners.html', {'places': location, 'relatives': relatives, 'books':books, 'owner':owner, 'locations':location})

def texts(request, text_id):
    # text_id is the title of a text
    text = Text.objects.get(title=text_id)
    books = Book.objects.filter(text=text)
    languages = text.language.all()
    tags = text.tags.all()
    places = []
    dates = []
    # Geo data for the map
    for book in books:
        locations = book.book_location.all()
        for location in locations:
            # For every book the text is in add the locations of that book
            places.append(location)
        toAdd = book.owner_info.all()
        for date in toAdd:
            # Add DateOwned objects to a list for display
            dates.append(date)
    return render(request, 'texts.html', {'text': text, 'books': books, 'languages': languages, 'tags': tags, 'places': places, 'dates' : dates})

def loadup(request):
    # Inactive- used for database loading
    return HttpResponse('Success')

# Inactive- to be used for autocomplete
#class BooksAutocomplete(autocomplete.Select2QuerySetView):
 #   def get_queryset(self):
  #      qs = Book.objects.all()

   #     if self.q:
    #        qs = qs.filter(shelfmark__istartswith=self.q)

     #   return qs

