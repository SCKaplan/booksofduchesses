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
]
