from django.contrib.gis import admin
from django.contrib.gis.db import models 
from .models import Tag, Author, Owner, DateOwned, Book, Location, Text
from mapwidgets.widgets import GooglePointFieldWidget
from books_app.forms import *

class LocationAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = LocationAdminForm
        else:
            self.form = LocationAdminForm
        return super(LocationAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Location, LocationAdmin)

class BookAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['language']

admin.site.register(Book, BookAdmin)

class TextAdmin(admin.ModelAdmin):
    autocomplete_fields = ['book']

admin.site.register(Text, TextAdmin)


class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']

admin.site.register(Tag, TagAdmin)
# Register your models here.

admin.site.register(Author)
admin.site.register(Owner)
admin.site.register(DateOwned)

