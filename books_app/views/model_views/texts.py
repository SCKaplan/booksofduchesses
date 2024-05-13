from dal import autocomplete
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from books_app.models import *
from books_app.forms import *

def texts(request, text_id):
    # text_id is the title of a text
    text = Text.objects.get(title=text_id)
    books = Book.objects.filter(text=text)
    languages = text.language.all()
    authors = text.authors.all()
    translators = text.translators.all()
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
    books_list = []
    for date in dates:
        books_list.append([date, date.ownership_type.all()])
    return render(
        request,
        "texts.html",
        {
            "text": text,
            "books": books,
            "languages": languages,
            "tags": tags,
            "places": places,
            "dates": dates,
            "authors": authors,
            "translators": translators,
            "books_list": books_list,
        },
    )


    
class TextAutocompete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Text.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q)
        return qs