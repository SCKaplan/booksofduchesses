from django import forms
from books_app.models import *
from django_select2.forms import Select2MultipleWidget
from django.forms import ModelChoiceField
from dal import autocomplete
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget
from captcha.fields import ReCaptchaField


class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
        widgets = {
            "geom": GooglePointFieldWidget(
                settings={"GooglePointFieldWidget": (("zoom", 8),)}
            )
        }


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
        widgets = {
            "geom": GooglePointFieldWidget(
                settings={"GooglePointFieldWidget": (("zoom", 8),)}
            )
        }


class LanguageAdminForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = "__all__"
        widgets = {
            "geom": GooglePointFieldWidget(
                settings={"GooglePointFieldWidget": (("zoom", 8),)}
            )
        }


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"
        widgets = {
            "geom": GooglePointFieldWidget(
                settings={"GooglePointFieldWidget": (("zoom", 8),)}
            )
        }


class OwnerAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
        widgets = {
            "geom": GooglePointFieldWidget(
                settings={"GooglePointFieldWidget": (("zoom", 8),)}
            )
        }


class OwnerPlaceDateLivedAdminForm(forms.ModelForm):
    class Meta:
        model = OwnerPlaceDateLived
        fields = "__all__"
        widgets = {
            "geom": GooglePointFieldWidget(
                settings={"GooglePointFieldWidget": (("zoom", 8),)}
            )
        }


class BookLocationAdminForm(forms.ModelForm):
    class Meta:
        model = BookLocation
        fields = "__all__"
        widgets = {
            "geom": GooglePointFieldWidget(
                settings={"GooglePointFieldWidget": (("zoom", 8),)}
            )
        }


def get_choice_list():
    return [book.shelfmark for book in Book.objects.all()]


ORDER_CHOICES = [
    ("alphabetical", "Alphabetical"),
    ("datedesc", "Descending date"),
    ("dateasc", "Ascending date"),
]


class OwnerLocationOrderForm(forms.Form):
    order_option = forms.ChoiceField(
        label="Order by", widget=forms.RadioSelect(choices=ORDER_CHOICES)
    )


class SearchForm(forms.Form):
    search = forms.CharField(label="Search", max_length=100, required=False)
    start_date = forms.CharField(label="Start Date", max_length=100, required=False)
    end_date = forms.CharField(label="End Date", max_length=100, required=False)
    owner = forms.CharField(label="Owner", max_length=100, required=False)
    shelfmark = forms.CharField(label="Shelfmark", max_length=100, required=False)
    # shelfmark = forms.ModelChoiceField(
    #   queryset=Book.objects.all(),
    #  widget=autocomplete.ModelSelect2Multiple(url='books-autocomplete')
    # )

    #    shelfmark = autocomplete.Select2ListCreateChoiceField(
    #       choice_list = get_choice_list,
    #      required=False,
    #     widget=autocomplete.ListSelect2(url='books-autocomplete')
    # )
    text = forms.CharField(label="Text", max_length=100, required=False)
    language = forms.CharField(label="Language", max_length=100, required=False)
    author = forms.CharField(label="Author", max_length=100, required=False)
    genre = forms.CharField(label="Genre", max_length=100, required=False)
    book_or_owner = [("owners", "Owners (default)"), ("books", "Books")]
    display = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple, choices=book_or_owner
    )


class BookForm(forms.ModelForm):
    new_captcha = ReCaptchaField(required=True)
    email = forms.EmailField(
        max_length=128,
        help_text="Valid contact information is required to approve your submission",
        required=True,
    )
    text = forms.CharField(
        max_length=128, help_text="Text(s) contained within the book", required=False
    )
    scribes = forms.CharField(max_length=128, required=False)
    illuminators = forms.CharField(max_length=128, required=False)
    printer = forms.CharField(max_length=128, required=False)
    book_location = forms.CharField(
        max_length=128,
        widget=forms.Textarea,
        help_text="List known locations and date at those locations",
        required=False,
    )
    owner_info = forms.CharField(
        max_length=128,
        help_text="Provide a list of owners and their dates of book ownership (if known)",
        widget=forms.Textarea,
        required=False,
    )
    bibliography = forms.CharField(
        max_length=128,
        help_text="Cite your sources",
        required=False,
        widget=forms.Textarea,
    )

    class Meta:
        model = Book
        fields = [
            "image",
            "shelfmark",
            "about",
            "text",
            "type",
            "ex_libris",
            "date_created",
            "catalog_entry",
            "digital_version",
            "scribes",
            "illuminators",
            "printer",
            "book_location",
            "owner_info",
            "bibliography",
        ]

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update({"class": "myfieldclass"})


class OwnerForm(forms.ModelForm):
    new_captcha = ReCaptchaField(required=True)
    email = forms.EmailField(
        max_length=128,
        help_text="Valid contact information is required to approve your submission",
        required=True,
    )
    books = forms.CharField(
        max_length=128,
        help_text="List books owned, preferably with dates and any geographic information",
        required=False,
        widget=forms.Textarea,
    )
    location = forms.CharField(
        max_length=128,
        help_text="List known owner locations",
        required=False,
        widget=forms.Textarea,
    )
    relatives = forms.CharField(
        max_length=128,
        help_text="List known relatives/family",
        required=False,
        widget=forms.Textarea,
    )

    class Meta:
        model = Owner
        fields = [
            "image",
            "image_citation",
            "bio",
            "name",
            "titles",
            "birth_year",
            "death_year",
            "gender",
            "motto",
            "symbol",
            "arms",
            "arms_citation",
            "signatures",
            "signatures_citation",
        ]

    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
