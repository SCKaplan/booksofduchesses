from dal import autocomplete
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from books_app.models import *
from books_app.forms import SearchForm

# Create your views here.
# Disclaimer: this doesn't seem efficient but this version runs the fastest
def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        search_form = SearchForm(request.POST)
        # check whether it's valid:
        if search_form.is_valid():
            # Get form data
            display = request.POST.getlist('display')
            query = request.POST.get('search', '')
            author = request.POST.get('author', '')
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            tag = request.POST.get('tag', '')
            text = request.POST.get('text', '')
            shelfmark = request.POST.get('shelfmark', '')
            owners_search = request.POST.get('owner', '')

            # Get books matching shelfmark search, all books if blank
            books_objs = Book.objects.filter(shelfmark__icontains=shelfmark)

	        # Author Search Field
            author_result = Author.objects.filter(name__icontains=author)
            texts_from_author = []
            books_from_author = []
            # For all the authors in a search result, add the texts which correspond to them
            for auth in author_result:
                text_query = Text.objects.filter(author=auth)
                for element in text_query:
                    texts_from_author.append(element)
            # Find all books in which each text appears
            for text_obj in texts_from_author:
                book = Book.objects.filter(text=text_obj)
                for b in book:
                    books_from_author.append(b)
            # Modifies books_objs to be only the elements that appear in both lists
            if len(author) != 0:
                books_objs = set(books_from_author) & set(books_objs)

            # Text Search Field- abbreviated version of author process
            texts_from_text = Text.objects.filter(title__icontains=text)
            books_from_text = []
            for item in texts_from_text:
                book = Book.objects.filter(text=item)
                for c in book:
                    books_from_text.append(c)
            if len(text) != 0:
                books_objs = set(books_from_text) & set(books_objs)

            # Tag Search Field- same as author, but tags are ManyToManyField
            if len(tag) != 0:
                texts_from_tag = []
                books_from_tag = []
                tag_result = Tag.objects.filter(tag__icontains=tag)
                all_texts = Text.objects.all()
                # Add the texts that have each tag
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
            # For the purpose of populating the search results
            else:
                texts_from_tag = Text.objects.all()

            # BookLocations for every book- we need a list of locations to map and date filter
            z = []
            books_to_filter = []
            for book in books_objs:
                z.append(book.book_location.all().order_by('date'))
            # z is a list of querysets, so we need to unpack
            for locs in z:
                for loc in locs:
                    books_to_filter.append(loc)

            # Owner Search Field
            owners_objs = Owner.objects.filter(name__icontains=owners_search)

            # Per profs. request- if user searches for texts the owners which owned those texts must appear
            # on the map as well
            owners_from_books = []
            # If we got any query about texts/books
            if len(shelfmark) != 0 or len(text) != 0 or len(author) != 0 or len(tag) != 0:
                # For every book we find the dates of ownership
                for book_obj in books_objs:
                    date_for_owner = DateOwned.objects.filter(book_owned=book_obj)
                    for owner_date in date_for_owner:
                        owners_from_books.append(owner_date.book_owner)
                # Compare the owners from their independent search and the owners from the book search- get duplicates
                owners_objs = set(owners_from_books) & set(owners_objs)

            # OwnerPlaceDateLived for each owner- we need a list of locations to map and date filter
            t = []
            owner_to_filter = []
            for owner in owners_objs:
                t.append(owner.owner_location.all().order_by('date_at_location'))
            for queryset in t:
                for item in queryset:
                    owner_to_filter.append(item)

            # Display options
            if len(display) == 0 or (display[0] == 'owners' and len(display) != 2):
                # If we only want to display owners
                books_to_filter = []
            if len(display) == 1 and display[0] == 'books':
                # If we only want to display books
                owner_to_filter = []

            # Get a date range- a list of a start date and end date in datetime format
            searchRange = []
            # Check for non-year formatting, i.e. if not len(4) and if any numbers are in string
            if len(start_date) != 4 or any(char.isalpha() for char in start_date):
                # Default date otherwise
                searchRange.append(datetime.datetime(1350, 1, 1))
            else:
                searchRange.append(datetime.datetime(int(start_date), 1, 1))
            if len(end_date) != 4 or any(char.isalpha() for char in end_date):
                searchRange.append(datetime.datetime(1500, 1, 1))
            else:
                searchRange.append(datetime.datetime(int(end_date), 1, 1))

            # Date range search field- filtered by BookLocation and OwnerPlaceDateLived objects
            books_final = []
            for date in books_to_filter:
                dateRange = date.date_range()
                # decide to display each book or not by comparing list of datetimes for overlap
                if not(dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    books_final.append(date)

	        # Same process for each OwnerPlaceDateLived
            owners_final = []
            for owner_date in owner_to_filter:
                dateRange = owner_date.date_range()
                if not(dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    owners_final.append(owner_date)

            # Helps display search results by reverse querying
            owners_search = []
            for owner_location in owners_final:
                 toAppend = Owner.objects.get(owner_location=owner_location)
                 owners_search.append(toAppend)
            # Black magic, don't touch
            owners_search = list(set(owners_search))

            books_search = []
            for book_location in books_final:
                 toAdd = Book.objects.get(book_location=book_location)
                 books_search.append(toAdd)
            books_search = list(set(books_search))

            # For displaying information about the search
            owner_len = len(owners_search)
            book_len = len(books_search)
            texts_search = set(texts_from_text) & set(texts_from_tag) & set(texts_from_author)
            text_len = len(texts_search)

            return render(request, 'index.html',{'books_search': books_search, 'owners_search': owners_search, 'search_form': search_form, 'owners': owners_final, 'display':display, 'books': books_final, 'book_len': book_len, 'owner_len': owner_len, 'text_len': text_len, 'texts_search': texts_search,})

    # if a GET (or any other method) we'll create a blank form
    else:
        # Default display is all female owners
        books = []
        locations = Location.objects.all()
        authors = Author.objects.all()
        owners = Owner.objects.filter(gender="Female")
        owners_default = []
        for owner in owners:
            toAdd = owner.owner_location.all()
            for item in toAdd:
                owners_default.append(item)
        search_form = SearchForm()

        return render(request, 'index.html',{'books':books, 'locations':locations, 'search_form': search_form, 'authors': authors, 'owners':owners_default})

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
class BooksAutocomplete(autocomplete.Select2ListView):
    def create(self, text): # To create a new object
        return text

    def get_list(self):
        list = [book.shelfmark for book in Book.objects.all()]

        if self.q:
            filter_result = Book.objects.all().filter(shelfmark__icontains=self.q)
            list = [book.shelfmark for book in filter_result]
        return list
