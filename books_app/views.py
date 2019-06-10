from django.shortcuts import render

from .models import Book

# Create your views here.

def index(request):

    f = open('/File/Path/To/.csv', 'r')
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

    authors = open('/File/Path/To Authors/.csv', 'r')
    for line in authors:
        line =  line.split(',')
        tmp = Author.objects.create()
        tmp.name = line[0]
        tmp.save()

    authors.close()

    owners = open('/File/Path/To Owners/.csv', 'r')
    for line in owners:
        line =  line.split(',')
        tmp = Owner.objects.create()
        tmp.name = line[0]
        tmp.motto = line[1]
        tmp.symbol = line[2]
        tmp.save()

    owners.close()

    text = open('/File/Path/To Texts/.csv', 'r')
    for line in text:
        line =  line.split(',')
        tmp = Text.objects.create()
        tmp.name = line[0]
        tmp.name_eng = line[1]
        tmp.save()

    text.close()
