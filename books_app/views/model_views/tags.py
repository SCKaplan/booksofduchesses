from dal import autocomplete
from books_app.models import *
from books_app.forms import *

class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter()