from django.contrib.gis.db import models
import datetime

# Create your models here.

class Tag(models.Model):
	geom = models.PointField(null=True, blank=True)
	tag = models.CharField(max_length=200)
	
	def __str__(self):
		return self.tag


class BooksLanguage(models.Model):
	books_language = models.CharField(max_length=200)
	geom = models.PolygonField(null=True, blank=True)

	def __str__(self):
		return self.books_language


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
	language = models.ManyToManyField('BooksLanguage', blank=True)

	def __str__(self):
		return self.title


class Author(models.Model):
	geom = models.PointField(null=True, blank=True)
	name = models.CharField(max_length=200)
	abstract = models.TextField(blank=True)
	birth_date = models.CharField(max_length=200, blank=True)
	death_date = models.CharField(max_length=200, blank=True)
	gender = models.CharField(max_length=200, blank=True)

	@property
	def popupcontent(self):
		return '{} {} {} {} {}'.format(self.name, self.abstract, self.birth_date, self.death_date, self.gender)

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

	@property
	def popupcontent(self):
		return '{} {} {}'.format(self.name,self.City,self.Country)

	def __str__(self):
		return self.name

class Owner(models.Model):
	geom = models.PointField(null=True, blank=True)
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
		
	def date_range(self):
		from datetime import datetime, timedelta
		dates = self.dateowned.split('-')
		month = "January"
		day = 1
		year = 1400
		final = []
		chop = 0
		if len(dates[0]) == 0 and len(dates[1]) == 0:
			# If we just get a dash what do we do?
			return "undetermined date"

		for date in dates:
			# How we want to organize uncertain dates
			if date.find('?') != -1 and len(date) < 2:
				print("what to do when its just a ?")
				date = "2019"
			if date.find('?') != -1:
				# Maybe add an uncertainty factor to this
				date = date.replace("?", "")
			if "c. " in date:
				# Maybe do a +/- operation to just get a range straight off the bat
				# For now just chop
				date = date.replace("c. ", "")
				date = date.replace("c.", "")
			if date.find('/') != -1:
				chop = date.index('/')
				date = date[:chop]
			# We now have a certain date
			date = date.split(' ')
			# If we have a full date
			if len(date[0]) < 3:
				day = date[0]
				month = date[1]
				year = date[2]
			# Just a month and year
			elif len(date) == 2:
				month = date[0]
				year = date[1]
			# Just a year
			else:
				year = date[0]

		stringIt = str(year) + "-" + month + "-" + str(day)
		final.append(datetime.strptime(stringIt, "%Y-%B-%d"))

		if len(final) == 1:
			# If we are only given one date, how far do we stretch the window (currently 2 yrs)
			final.append(final[0] + timedelta(days=731))
			final[0] = final[0] - timedelta(days=730)
		return final


	def __str__(self):
		return self.dateowned
