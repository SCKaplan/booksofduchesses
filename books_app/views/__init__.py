from dal import autocomplete
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from books_app.models import *
from books_app.forms import *


# Create your views here.
# Disclaimer: this doesn't seem efficient but this version runs the fastest
def index(request):
    texts_about = Text.objects.all().count()
    owners_about = Owner.objects.filter(gender="Female").count()
    books_about = Book.objects.filter(reviewed=True).count()
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        search_form = SearchForm(request.POST)
        # check whether it's valid:
        if search_form.is_valid():
            # Get form data
            display = request.POST.getlist("display")
            query = request.POST.get("search", "")
            author = request.POST.get("author", "")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")
            tag = request.POST.get("genre", "")
            text = request.POST.get("text", "")
            #language = request.POST.get("language", "")
            shelfmark = request.POST.get("shelfmark", "")
            owners_search = request.POST.get("owner", "")
            # Get books matching shelfmark search, all books if blank
            books_objs = Book.objects.filter(shelfmark__icontains=shelfmark)
        
            # Author Search Field
            author_result = Author.objects.filter(name__icontains=author)
            texts_from_author = []
            books_from_author = []
            # For all the authors in a search result, add the texts which correspond to them
            if len(author) == 0:
                texts_from_author = Text.objects.all()
            else:
                for t in Text.objects.all():
                    if set(author_result) & set(t.authors.all()):
                        texts_from_author.append(t)

            # Find all books in which each text appears
            for text_obj in texts_from_author:
                book = Book.objects.filter(text=text_obj)
                for b in book:
                    books_from_author.append(b)
            # Modifies books_objs to be only the elements that appear in both lists
            if len(author) != 0:
                books_objs = set(books_from_author) & set(books_objs)

            # Text Search Field- abbreviated version of author process
            texts_from_text = list(
                set(Text.objects.filter(title__icontains=text))
                | set(Text.objects.filter(name_eng__icontains=text))
            )
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
                for a in Text.objects.all():
                    if set(tag_result) & set(a.tags.all()):
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
                z.append(book.book_location.all().order_by("date"))
            # z is a list of querysets, so we need to unpack
            for locs in z:
                for loc in locs:
                    books_to_filter.append(loc)

            # Owner Search Field
            owners_objs = Owner.objects.filter(name__icontains=owners_search)

            books_from_owners = []
            for owners_obj in owners_objs:
                books_from_owners.append(
                    BookLocation.objects.filter(owner_at_time=owners_obj)
                )
            books_from_owners1 = []
            for query in books_from_owners:
                for lst in query:
                    books_from_owners1.append(lst)
            books_to_filter = list(set(books_from_owners1) & set(books_to_filter))
            # Per profs. request- if user searches for texts the owners which owned those texts must appear
            # on the map as well
            owners_from_books = []
            # If we got any query about texts/books
            if (
                len(shelfmark) != 0
                or len(text) != 0
                or len(author) != 0
                or len(tag) != 0
            ):
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
                t.append(owner.owner_location.all().order_by("date_at_location"))
            for queryset in t:
                for item in queryset:
                    owner_to_filter.append(item)

            # Display options
            if len(display) == 0 or (display[0] == "owners" and len(display) != 2):
                # If we only want to display owners
                books_to_filter = []
            if len(display) == 1 and display[0] == "books":
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
                if not (dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    books_final.append(date)

            # Same process for each OwnerPlaceDateLived
            owners_final = []
            for owner_date in owner_to_filter:
                dateRange = owner_date.date_range()
                if not (dateRange[1] < searchRange[0] or dateRange[0] > searchRange[1]):
                    owners_final.append(owner_date)

            # Helps display search results by reverse querying
            owners_search = []
            for owner_location in owners_final:
                toAppend = Owner.objects.get(owner_location=owner_location)
                owners_search.append(toAppend)
            # Get rid of duplicates
            owners_search = list(set(owners_search))
            owner_len = len(owners_search)
            owners_search_preview = []
            if owner_len > 5:
                owners_search_preview = owners_search[:5]
                owners_search = owners_search[5:]

            books_search = []
            for book_location in books_final:
                toAdd = Book.objects.get(book_location=book_location)
                books_search.append(toAdd)
            books_search = list(set(books_search))
            book_len = len(books_search)
            books_search_preview = []
            if book_len > 5:
                books_search_preview = books_search[:5]
                books_search = books_search[5:]

            # For displaying information about the search
            texts_from_books = []
            q = []
            for v in books_search:
                q.append(v.text.all())
            for textquery in q:
                for listing in textquery:
                    texts_from_books.append(listing)
            texts_search = list(
                set(texts_from_text) & set(texts_from_tag) & set(texts_from_author)
            )
            if not (author or tag or text):
                texts_search = list(set(texts_search).union(set(texts_from_books)))
            if not (books_search or owners_search) and not (author or text or tag):
                texts_search = []
            texts_search_preview = []
            text_len = len(texts_search)
            if text_len > 5:
                texts_search_preview = texts_search[:5]
                texts_search = texts_search[5:]
            display_search = True

            return render(
                request,
                "index.html",
                {
                    "books_search": books_search,
                    "owners_search": owners_search,
                    "search_form": search_form,
                    "owners": owners_final,
                    "display": display,
                    "books": books_final,
                    "book_len": book_len,
                    "owner_len": owner_len,
                    "text_len": text_len,
                    "texts_search": texts_search,
                    "books_search_preview": books_search_preview,
                    "owners_search_preview": owners_search_preview,
                    "texts_search_preview": texts_search_preview,
                    "display_search": display_search,
                    "books_about": books_about,
                    "owners_about": owners_about,
                    "texts_about": texts_about,
                },
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        # Default display is all female owners
        # owner_locations = [opdl.the_place for opdl in OwnerPlaceDateLived.objects.filter(owner__in=Owner.objects.filter(gender__exact="Female"))]

        return render(
            request,
            "index.html",
            {
                "books": [],
                "search_form": SearchForm(),
                "owners": [],
                "display_search": False,
                "books_about": books_about,
                "owners_about": owners_about,
                "texts_about": texts_about,
            },
        )


def loadup(request):
    # Inactive- used for database loading
    return HttpResponse("Success")


def search(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
    else:
        search_form = SearchForm()
        dates = DateOwned.objects.all()
        owners = Owner.objects.all()
        books = Book.objects.all()
        texts = Text.objects.all()

    return render(
        request,
        "search.html",
        {
            "search_form": search_form,
            "dates": dates,
            "owners": owners,
            "books": books,
            "texts": texts,
        },
    )


def teach(request):
    return render(request, "teach.html")


def about(request):
    about = About.objects.all()
    about = [about[0], about[1], about[2], about[3]]
    return render(request, "about.html", {"about": about})


def suggest_sel(request):
    return render(request, "suggest_sel.html", {})


def bibliography(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
    else:
        search_form = SearchForm()
        bibs = Bibliography.objects.all().values('source', 'author_date').distinct()
    return render(
        request, "bibliography.html", {"search_form": search_form, "bibs": bibs}
    )
