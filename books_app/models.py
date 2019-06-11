from django.contrib.gis.db import models
from djgeojson.fields import PointField
import datetime

# Create your models here.

class Tag(models.Model):
	tag = models.CharField(max_length=200)
	
	def __str__(self):
		return self.tag

class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True)
	owner = models.ManyToManyField('Owner', blank=True)
	type = models.CharField(max_length=200, blank=True)
	ex_libris = models.CharField(max_length=200, blank=True) # can link to more books?
	bibliography = models.CharField(max_length=200, blank=True)
	library = models.ForeignKey('Location', blank=True, on_delete=models.SET_NULL, null=True) # Should reference a location
	digital_version = models.CharField(max_length=200, blank=True)
	date_created= models.CharField(max_length=200, blank=True, null=True)
	book_movements = models.CharField(max_length=200, blank=True)
	scribes = models.CharField(max_length=200, blank=True)
	illuminators = models.CharField(max_length=200, blank=True)
	language = models.ManyToManyField('Tag', blank=True)

	def __str__(self):
		return self.title

class Author(models.Model):
	name = models.CharField(max_length=200)
	abstract = models.TextField(blank=True)
	birth_date = models.CharField(max_length=200, blank=True)
	death_date = models.CharField(max_length=200, blank=True)
	gender = models.CharField(max_length=200, blank=True)

	# Link needed?
	def __str__(self):
		return self.name


class Text(models.Model):
	name = models.CharField(max_length=200)
	name_eng = models.CharField(max_length=200, blank=True)
	tags = models.ManyToManyField(Tag)
	book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
	def __str__(self):
		return self.name

class Location(models.Model):
	geom = models.PointField(null=True, blank=True)
	name =  models.CharField(max_length=200)
	City =  models.CharField(max_length=200)
	Country =  models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Owner(models.Model):
	name = models.CharField(max_length=200)
	motto = models.CharField(max_length=200, blank=True, null=True)
	symbol = models.CharField(max_length=200, blank=True, null=True)
	book_date = models.ManyToManyField('DateOwned', blank=True)
	def __str__(self):
		return self.name

class DateOwned(models.Model):
	#owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
	book_owned = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True) #book_owned = models.ForeignKey(Book, on_delete=models.CASCADE)
	dateowned = models.CharField(max_length=200, null = True)
	Conf = 'Confirmed'
	Poss = 'Possible'
	conf_choices = [(Conf, "Confirmed"),(Poss, "Possible")]
	conf_or_possible = models.CharField(max_length=9, choices=conf_choices, default='Confirmed')
	class Meta:
		verbose_name = 'Date owned'
		verbose_name_plural = 'Dates owned'

	def __str__(self):
		return self.dateowned
