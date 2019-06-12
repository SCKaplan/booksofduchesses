from django import forms
from books_app.models import *

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


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)
    start_date = forms.CharField(label='Start Date', max_length=100, required=False)
    end_date = forms.CharField(label='End Date', max_length=100, required=False)
    owner = forms.CharField(label='Owner', max_length=100, required=False)
    shelfmark = forms.CharField(label='Shelfmark', max_length=100, required=False)
    text = forms.CharField(label='Text', max_length=100, required=False)
    author = forms.CharField(label='Author', max_length=100, required=False)
    genre = forms.CharField(label='Genre', max_length=100, required=False)

