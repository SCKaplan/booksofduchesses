from django.db import models
import datetime

# Create your models here.

class Tag(models.Model):
	tag = models.CharField(max_length=200)

class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	owner = models.ManyToManyField('DateOwned', blank=True)
	type = models.CharField(max_length=200)
	date = models.CharField(max_length=30)
	language = models.CharField(max_length=30)

class Author(models.Model):
	name = models.CharField(max_length=200)

class Owner(models.Model):
	name = models.CharField(max_length=200)

class DateOwned(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    book_owned = models.ForeignKey(Book, on_delete=models.CASCADE)
    dateowned = models.DateTimeField()

