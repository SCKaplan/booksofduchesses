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

# Register your models here.
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Owner)
admin.site.register(DateOwned)
admin.site.register(Book)
admin.site.register(Text)

