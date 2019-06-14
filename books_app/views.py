from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from books_app.models import *
from books_app.forms import SearchForm


# Create your views here.

def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        search_form = SearchForm(request.POST)
        # check whether it's valid:
        if search_form.is_valid():

            # Search queries for books, authors and owners
            query = request.POST.get('search', '')

            author_result = Author.objects.filter(name__icontains=query)
            owners_result = Owner.objects.filter(name__icontains=query)


            locations = Location.objects.filter(name__icontains=query)

            author = request.POST.get('author', '')
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            owner = request.POST.get('owner', '')
            genre = request.POST.get('genre', '')
            text = request.POST.get('text', '')
            shelfmark = request.POST.get('shelfmark', '')

            return render(request, 'index.html',
                          #{'books': books_result, 'locations': locations, 'search_form': search_form, 'authors': author_result, 'owners':owner_result}
                          {'locations': locations, 'search_form': search_form, 'authors': author_result, 'owners':owners_result, }
                        )

    # if a GET (or any other method) we'll create a blank form
    else:
        books = Book.objects.all()
        locations = Location.objects.all()
        authors = Author.objects.all()
        owners = Owner.objects.all()
        search_form = SearchForm()

        return render(request, 'index.html',{'books':books, 'locations':locations, 'search_form': search_form, 'authors': authors, 'owners':owners})
    # 
    # f = open('/Users/FreddieGould/Downloads/books.csv', 'r')
    # for line in f:
    #     line =  line.split(',')
    #     tmp = Book.objects.create()
    #     tmp.title = line[0]
    #     tmp.date_created = line[1]
    #     tmp.scribes = line[2]
    #     tmp.illuminators = line[3]
    #     tmp.digital_version = line[4]
    #     tmp.save()
    # 
    # f.close()
    # 
    # authors = open('/Users/FreddieGould/Downloads/authors.csv', 'r')
    # for line in authors:
    #     line =  line.split(',')
    #     tmp = Author.objects.create()
    #     tmp.name = line[0]
    #     tmp.save()
    # 
    # authors.close()
    # 
    # owners = open('/Users/FreddieGould/Downloads/owners.csv', 'r')
    # for line in owners:
    #     line =  line.split(',')
    #     tmp = Owner.objects.create()
    #     tmp.name = line[0]
    #     tmp.motto = line[1]
    #     tmp.symbol = line[2]
    #     tmp.save()
    # 
    # owners.close()
    # 
    # text = open('/Users/FreddieGould/Downloads/texts.csv', 'r')
    # for line in text:
    #     line =  line.split(',')
    #     tmp = Text.objects.create()
    #     tmp.name = line[0]
    #     tmp.name_eng = line[1]
    #     tmp.save()
    # 
    # text.close()
   
def loadup(request):
    textinfo = open('/Path/To/CSV/texts2.csv', 'r')
    texts = Text.objects.all()
    textsIndex = 0
    for line in textinfo:
        line = line.split(',')
        toEdit = texts[textsIndex + 1]
        # Text name, Books, name_eng, author, arlima, tags order in csv
        # name, name_eng, arlima are all charfields
        toEdit.name = line[0]
        toEdit.name_eng = line[2]
        toEdit.arlima = line[4]
        # Author is a Foreign Key so make an object
        author = Author.objects.filter(name__contains = line[3])
        if len(author) != 0:
            toEdit.author = author[0]
        # Tags Many to Many Fields
        allTags = line[5][:-1]
        allTags = allTags.split('.')
        for tag in allTags:
            tag = tag.lstrip()
            if len(tag) != 0:
                toAdd = Tag.objects.filter(tag__contains=tag)
                toEdit.tags.add(toAdd[0])
        toEdit.save()
        # Books Many to Many Field
        allBooks = line[1]
        allBooks = allBooks.split('!')
        for book in allBooks:
            book = book.lstrip()
            if len(book) != 0:
                toAdd = Book.objects.filter(title__contains=book)
                # So that we don't break it, for now
                if len(toAdd) != 0:
                    toEdit.book.add(toAdd[0])
                else:
                    print("This is a book that is not yet loaded into the db")
        toEdit.save()

        textsIndex += 1
    textinfo.close()

