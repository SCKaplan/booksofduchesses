from dal import autocomplete
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from books_app.models import *
from books_app.forms import *

def to_valid_search_form(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            return search_form
    return None

def parseYear(year_string, defaultYear):
    try:
        return datetime.datetime(int(year_string), 1, 1)
    except ValueError:
        return datetime.datetime(defaultYear, 1, 1)


# Get a date range- a list of a start date and end date in datetime format
def to_search_range(start_date_qry, end_date_qry):                
    return [
        parseYear(start_date_qry, 1300), 
        parseYear(end_date_qry, 1600)
    ]

def in_search_range(search_range, range):
    return not (range[1] < search_range[0] or range[0] > search_range[1])

def scope_books_to_timerange(search_range, books):
    if(search_range == UNIVERSAL_DATE_RANGE):
        return books
    return [book for book in books for owner_info in book.owner_info.all() if in_search_range(search_range, owner_info.date_range())]



# Create your views here.
def index(request):
    texts_about = Text.objects.count()
    owners_about = Owner.objects.filter(gender="Female").count()
    books_about = Book.objects.filter(reviewed=True).count()
    search_form = to_valid_search_form(request)
    if search_form:
        author = request.POST.get("author", "")
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")
        tag = request.POST.get("genre", "")
        text = request.POST.get("text", "")
        language = request.POST.get("language", "")
        shelfmark = request.POST.get("shelfmark", "")
        owner = request.POST.get("owner", "")

        # Get books matching shelfmark search, all books if blank
        owners_qs = Owner.objects.filter(
            Q(name__icontains=owner) | Q(titles__icontains=owner)
        )
        books_qs = Book.objects.filter(shelfmark__icontains=shelfmark)

        # Text Search Fields
        texts_qs = Text.objects.filter(
            authors__name__icontains=author,
            language__books_language__icontains=language
        ).filter(
            Q(title__icontains=text) | Q(name_eng__icontains=text)
        ).filter(tags__tag__icontains=tag)

        books_results = books_qs.filter(owner_info__book_owner__in=owners_qs).filter(text__in=texts_qs).distinct()
        
        # This is hacky and slow but needed until we get real date data in the db
        search_range = to_search_range(start_date, end_date)
        books_results = scope_books_to_timerange(search_range, books_results)

        texts_results = texts_qs.filter(book__in=books_results).distinct()
        owners_results = owners_qs.filter(dateowned__book_owned__in=books_results).distinct()
        book_locations = list(set(location.book_location for book in books_results for location in book.book_location.all()))
        owner_locations = list(set(location.the_place for owner in owners_results for location in owner.owner_location.all()))
        
        return render(
            request,
            "index.html",
            {
            "books_search": sorted(books_results, key=lambda b: b.shelfmark),
            "owners_search": sorted(owners_results, key=lambda o: "{} {}".format(o.name, o.titles)),
            "texts_search": sorted(texts_results, key=lambda t: t.title),
            "search_form": search_form,
            "owners": owner_locations,
            "books": book_locations,
            "display_search": True,
            "books_about": books_about,
            "owners_about": owners_about,
            "texts_about": texts_about,
            }
        )


    # if a GET (or any other method) we'll create a blank form
    else:
        # Default display is all female owners
        owner_places_qs = OwnerPlaceDateLived.objects.filter(owner__in=Owner.objects.filter(gender__exact="Female"))
        owner_locations = list(set(location.the_place for location in owner_places_qs.all()))
        return render(
            request,
            "index.html",
            {
                "books": [],
                "search_form": SearchForm(),
                "owners": owner_locations,
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
