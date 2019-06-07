from django.shortcuts import render

from .models import Book

# Create your views here.

def index(request):

    f = open('/Users/FreddieGould/Downloads/book_title - Sheet1.csv', 'r')
    for line in f:
        line =  line.split(',')
        tmp = Book.objects.create()
        tmp.title = line[0]
        tmp.date_created = line[1]
        tmp.scribes = line[2]
        tmp.illuminators = line[3]
        tmp.digital_version = line[4]
        tmp.save()

    f.close()
