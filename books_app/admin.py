from django.contrib.gis import admin
from django.contrib.gis.db import models
from .models import *
from mapwidgets.widgets import GooglePointFieldWidget
from books_app.forms import *

# If you want to add search capabilities within the admin follow the search_field examples
# If you want to add autocomplete fields within the admin (for editing/adding models) follow the corresponsing examples
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = LocationAdminForm
        else:
            self.form = LocationAdminForm
        return super(LocationAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Location, LocationAdmin)


class BookAdmin(admin.ModelAdmin):
    search_fields = ['shelfmark']
    autocomplete_fields = ['text', 'bibliography', 'book_location', 'owner_info', 'scribes', 'illuminators']
    ordering = ('shelfmark',)

admin.site.register(Book, BookAdmin)


class TextAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['tags', 'language', 'authors', 'translators']

admin.site.register(Text, TextAdmin)


class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = TagAdminForm
        else:
            self.form = TagAdminForm
        return super(TagAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Tag, TagAdmin)
# Register your models here.


class OwnerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['book_date', 'relation','owner_location']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = OwnerAdminForm
        else:
            self.form = OwnerAdminForm
        return super(OwnerAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Owner, OwnerAdmin)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = AuthorAdminForm
        else:
            self.form = AuthorAdminForm
        return super(AuthorAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Author, AuthorAdmin)


class DateOwnedAdmin(admin.ModelAdmin):
    search_fields =['book_owned__shelfmark', 'book_owner__name']
    autocomplete_fields = ['book_owned', 'book_owner', 'ownership_type']
    list_display = ['dateowned', 'book_owned', 'book_owner']
    list_filter = ('book_owner','book_owned')

admin.site.register(DateOwned, DateOwnedAdmin)


class BooksLanguageAdmin(admin.ModelAdmin):
    search_fields = ['books_language']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = BooksLanguageAdminForm
        else:
            self.form = BooksLanguageAdminForm
        return super(BooksLanguageAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(BooksLanguage, BooksLanguageAdmin)

class OwnerPlaceDateLivedAdmin(admin.ModelAdmin):
    search_fields = ['the_place']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = OwnerPlaceDateLivedAdminForm
        else:
            self.form = OwnerPlaceDateLivedAdminForm
        return super(OwnerPlaceDateLivedAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(OwnerPlaceDateLived, OwnerPlaceDateLivedAdmin)

class BibliographyAdmin(admin.ModelAdmin):
    search_fields = ['author_date']

admin.site.register(Bibliography, BibliographyAdmin)

class RelativeAdmin(admin.ModelAdmin):
    search_fields = ['person']
    autocomplete_fields = ['person']

admin.site.register(Relative, RelativeAdmin)

class TranslatorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

admin.site.register(Translator, TranslatorAdmin)

class BookLocationAdmin(admin.ModelAdmin):
    search_fields = ['book_location__name', 'book_shelfmark__shelfmark']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = BookLocationAdminForm
        else:
            self.form = BookLocationAdminForm
        return super(BookLocationAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(BookLocation, BookLocationAdmin)

class IlluminatorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

admin.site.register(Illuminator, IlluminatorAdmin)

class ScribeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

admin.site.register(Scribe, ScribeAdmin)

class EvidenceAdmin(admin.ModelAdmin):
    search_fields = ['evidence', 'conf_or_possible']

admin.site.register(Evidence, EvidenceAdmin)
