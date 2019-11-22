from django.conf.urls import url
from django.urls import include, re_path
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
import books_app.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('loadup/', views.loadup, name='loadup'),
    # Django will expect a string and send it to the view as var owner_id
    path('books/<str:book_id>', views.books, name='books'),
    path('owners/<str:owner_id>/', views.owners, name='owners'),
    path('texts/<str:text_id>/', views.texts, name='texts'),
    path('books-autocomplete/', views.BooksAutocomplete.as_view(), name='books-autocomplete'),
    path('search', views.search, name='search')
]
