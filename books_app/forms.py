from django import forms
from books_app.models import *
from django_select2.forms import Select2MultipleWidget
from django.forms import ModelChoiceField
from dal import autocomplete
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget


class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
        widgets = {
            'geom':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
        widgets = {
            'geom':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }


class BooksLanguageAdminForm(forms.ModelForm):
    class Meta:
        model = BooksLanguage
        fields = "__all__"
        widgets = {
            'geom':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"
        widgets = {
            'geom':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }


class OwnerAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
        widgets = {
            'geom':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }

class OwnerPlaceDateLivedAdminForm(forms.ModelForm):
    class Meta:
        model = OwnerPlaceDateLived
        fields = "__all__"
        widgets = {
            'geom':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }

class BookLocationAdminForm(forms.ModelForm):
    class Meta:
        model = BookLocation
        fields = "__all__"
        widgets = {
            'geom':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }

def get_choice_list():
    return [book.shelfmark for book in Book.objects.all()]

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)
    start_date = forms.CharField(label='Start Date', max_length=100, required=False)
    end_date = forms.CharField(label='End Date', max_length=100, required=False)
    owner = forms.CharField(label='Owner', max_length=100, required=False)
    shelfmark = forms.CharField(label='Shelfmark', max_length=100, required=False)
    #shelfmark = forms.ModelChoiceField(
     #   queryset=Book.objects.all(),
      #  widget=autocomplete.ModelSelect2Multiple(url='books-autocomplete')
    #)

#    shelfmark = autocomplete.Select2ListCreateChoiceField(
 #       choice_list = get_choice_list,
  #      required=False,
   #     widget=autocomplete.ListSelect2(url='books-autocomplete')
   # )
    text = forms.CharField(label='Text', max_length=100, required=False)
    author = forms.CharField(label='Author', max_length=100, required=False)
    genre = forms.CharField(label='Genre', max_length=100, required=False)
    book_or_owner = [
    ('owners', 'Owners (default)'),
    ('books', 'Books'),
]
    display = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=book_or_owner,
    )
