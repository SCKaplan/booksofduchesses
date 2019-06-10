from django.contrib import admin
from django.contrib.gis.db import models 
from .models import Tag, Author, Owner, DateOwned, Book, Location, Text
from mapwidgets.widgets import GooglePointFieldWidget

class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {'widget': GooglePointFieldWidget}
    }

# Register your models here.
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Owner)
admin.site.register(DateOwned)
admin.site.register(Book)
admin.site.register(Text)
admin.site.register(Location)

