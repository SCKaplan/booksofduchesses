from django.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
import books_app.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('loadup/', views.loadup, name='loadup'),
    path('bibload/', views.bibload, name='bibload'),
    #path('owners/', views.owners, name='owners'),
    # Django will expect a string and send it to the view as var owner_id
    path('books/<str:book_id>', views.books, name='books'),
    path('owners/<str:owner_id>/', views.owners, name='owners'),
]
