from dal import autocomplete
from books_app.models import *
from books_app.forms import *
    
class AuthorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Author.objects.all();
    
        if self.q:
            qs = qs.filter(name__icontains=self.q)