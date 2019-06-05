from django.db import models

# Create your models here.

class Tag(models.Model):
	tag = models.CharField(max_length=200)


class Book(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    date = models.CharField(max_length=30)
    language = models.CharField(max_length=30)
    tags = models.ManytoMany(Tag)


class Text(models.Model):
    title = models.CharField(max_length=30)
    english_title = models.CharField(max_length=30)
    language = models.CharField(max_length=30)
    tags = models.ManytoMany(Tag)


class TextinBook(models.Model):
    text = models.ForeignKey(Text)
    book = models.ManytoMany(Tag)
    page_range = models.CharField(max_length=30)


class Person(model.Model):
	book_owner = 
	text_author = 
	book_author = 