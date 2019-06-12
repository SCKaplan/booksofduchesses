from django.shortcuts import render
from django.http import HttpResponse


from books_app.models import *
from books_app.forms import SearchForm


# Create your views here.

def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        search_form = SearchForm(request.POST)
        # check whether it's valid:
        if search_form.is_valid():
            print(request.POST)
            search = request.POST.get('search', None)
            author = request.POST.get('author', None)
            start_date = request.POST.get('start_date', None)
            end_date = request.POST.get('end_date', None)
            owner = request.POST.get('owner', None)
            genre = request.POST.get('genre', None)
            text = request.POST.get('text', None)
            shelfmark = request.POST.get('shelfmark', None)

            books = Book.objects.filter()
            locations = Location.objects.all()
            authors = Author.objects.all()

            search_form = SearchForm()

            return render(request, 'index.html',
                          {'books': books, 'locations': locations, 'search_form': search_form, 'authors': authors})

    # if a GET (or any other method) we'll create a blank form
    else:
        books = Book.objects.all()
        locations = Location.objects.all()
        authors = Author.objects.all()

        search_form = SearchForm()

        return render(request, 'index.html',{'books':books, 'locations':locations, 'search_form': search_form, 'authors': authors})
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

