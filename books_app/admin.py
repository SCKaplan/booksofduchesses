from django.contrib import admin

from .models import Tag, Author, Owner, DateOwned, Book

# Register your models here.
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Owner)
admin.site.register(DateOwned)
admin.site.register(Book)
