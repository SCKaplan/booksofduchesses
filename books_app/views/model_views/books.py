from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.core.serializers import serialize
from books_app.models import *
from books_app.forms import *


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
    printers = book.printer.all()
    # For owners we query DateOwned objects because they contain dates which we need to be on template
    # orders by date_range method... i think
    owners_date = sorted(
        DateOwned.objects.filter(book_owned=book), key=lambda a: a.date_range()
    )
    date_list = []
    for date in owners_date:
        date_list.append([date, date.ownership_type.all()])
    # owners_date = DateOwned.objects.filter(book_owned=book).order_by('dateowned')
    owner_geo = []
    evidences = []
    for date in owners_date:
        try:
            # In case some misc dateowned objects appear- if everything has a link and we clean up this isn't necessary
            owner_geo.append(date)
            evidences.append([date, date.ownership_type.all()])
        except:
            pass
    return render(
        request,
        "books.html",
        {
            "book": book,
            "owners": owner_geo,
            "texts": texts,
            "bibs": bibs,
            "places": places,
            "iluminators": illuminators,
            "scribes": scribes,
            "printers": printers,
            "evidences": evidences,
            "date_list": date_list,
        },
    )

def suggest_book(request):
    if request.method == "POST":
        f = BookForm(request.POST)
        if f.is_valid():
            new_article = f.save(commit=False)
            text = request.POST.get("text", "")
            email = request.POST.get("email", "")
            scribes = request.POST.get("scribes", "")
            illuminators = request.POST.get("illuminators", "")
            printer = request.POST.get("printer", "")
            book_location = request.POST.get("book_location", "")
            owner_info = request.POST.get("owner_info", "")
            bibliography = request.POST.get("bibliography", "")

            new_article.comments = (
                "Submitter Contact Info: "
                + email
                + "\nText: "
                + text
                + "\nIlluminators: "
                + illuminators
                + "\nScribes: "
                + scribes
                + "\n"
            )
            new_article.comments += (
                "Printers: "
                + printer
                + "\nBook Locations: "
                + book_location
                + "\nOwner Info"
                + owner_info
                + "\n"
            )
            new_article.comments += "Bibliography: : " + bibliography + "\n"
            new_article.save()
            text = request.POST.get("text", "")
            return render(request, "suggested.html", {})
        else:
            book_form = BookForm()
            failed = True
            return render(
                request, "suggest_book.html", {"book_form": book_form, "failed": failed}
            )
    else:
        book_form = BookForm()
        failed = False
        return render(
            request, "suggest_book.html", {"book_form": book_form, "failed": failed}
        )

def books_shelfmark_autocomplete(request):
    term = request.GET.get('term', '')
    data = serialize('json', Book.objects.filter(shelfmark__icontains=term))
    return HttpResponse(data, content_type='application/json')

def books_owner_autocomplete(request):
    term = request.GET.get('term', '')
    owner_info = DateOwned.objects.filter(book_owner__name__icontains=term)
    data = serialize('json', [owner.book_owner for owner in owner_info])
    return HttpResponse(data, content_type='application/json')

def books_author_autocomplete(request):
    term = request.GET.get('term', '')
    authors = Author.objects.filter(name__icontains=term)
    data = serialize('json', [author for author in authors if author.text_set.all()])
    return HttpResponse(data, content_type='application/json')

def books_tag_autocomplete(request):
    term = request.GET.get('term', '')
    tags = Tag.objects.filter(tag__icontains=term)
    data = serialize('json', [tag for tag in tags if tag.text_set.all()])
    return HttpResponse(data, content_type='application/json') 

def books_language_autocomplete(request):
    term = request.GET.get('term', '')
    languages = BooksLanguage.objects.filter(books_language__icontains=term)
    data = serialize('json', languages)
    return HttpResponse(data, content_type='application/json') 
    
def books_text_autocomplete(request):
    term = request.GET.get('term', '')
    texts = Text.objects.filter(Q(title__icontains=term) | Q(name_eng__icontains=term))
    data = serialize('json', [text for text in texts if text.book_set.all()])
    return HttpResponse(data, content_type='application/json') 