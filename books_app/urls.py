from django.conf.urls import url
from django.urls import include, re_path
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
import books_app.views as views
from books_app.views.model_views import books as BookViews
from books_app.views.model_views import owners as OwnerViews
from books_app.views.model_views import texts as TextViews



urlpatterns = [
    path("", views.index, name="index"),
    path("loadup/", views.loadup, name="loadup"),
    # Django will expect a string and send it to the view as var owner_id
    path("books/<str:book_id>", BookViews.books, name="books"),
    path("owners/<str:owner_id>/", OwnerViews.owners, name="owners"),
    path("texts/<str:text_id>/", TextViews.texts, name="texts"),
    path(
        "books-shelfmark-autocomplete/",
        BookViews.books_shelfmark_autocomplete,
        name="books-shelfmark-autocomplete",
    ),
    path(
        "books-owner-autocomplete/",
        BookViews.books_owner_autocomplete,
        name="books-owner-autocomplete",
    ),
    path(
        "books-author-autocomplete/",
        BookViews.books_author_autocomplete,
        name="books-author-autocomplete",
    ),
    path(
        "books-tag-autocomplete/",
        BookViews.books_tag_autocomplete,
        name="books-tag-autocomplete",
    ),
    path(
        "books-text-autocomplete/",
        BookViews.books_text_autocomplete,
        name="books-text-autocomplete",
    ),
    path(
        "books-language-autocomplete/",
        BookViews.books_language_autocomplete,
        name="books-language-autocomplete",
    ),
    path("search", views.search, name="search"),
    path("about", views.about, name="about"),
    path("suggest", views.suggest_sel, name="suggest_sel"),
    path("suggest/book", BookViews.suggest_book, name="suggest_book"),
    path("suggest/owner", OwnerViews.suggest_owner, name="suggest_owner"),
    path("teach", views.teach, name="teach"),
    path("bibliography", views.bibliography, name="bibliography"),
    #    url(r'^captcha/', include('captcha.urls')),
]
