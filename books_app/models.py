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
	class Meta:
		verbose_name = 'Language'

	def __str__(self):
		return self.books_language

class Book(models.Model):
	image = models.ImageField(null=True, blank=True)
	shelfmark = models.CharField(max_length=200)
	owner = models.ManyToManyField('Owner', blank=True, verbose_name="Owner(s)")
	text = models.ManyToManyField('Text', blank=True, verbose_name="Text(s)")
	type = models.CharField(max_length=200, blank=True)
	ex_libris = models.TextField(blank=True) # can link to more books?
	bibliography = models.ManyToManyField('Bibliography', blank=True)
	library = models.ForeignKey('Location', blank=True, on_delete=models.SET_NULL, null=True) # Should reference a location
	digital_version = models.CharField(max_length=200, blank=True)
	date_created= models.CharField(max_length=200, blank=True, null=True)
	scribes = models.CharField(max_length=200, blank=True)
	illuminators = models.CharField(max_length=200, blank=True)
	catalog_entry = models.CharField(max_length=2000, blank=True)
	book_location = models.ManyToManyField('BookLocation', blank=True)
	def __str__(self):
		return self.shelfmark


class Author(models.Model):
	image = models.ImageField(null=True, blank=True)
	geom = models.PointField(null=True, blank=True)
	name = models.CharField(max_length=200)
	abstract = models.TextField("About", blank=True)
	birth_date = models.CharField(max_length=200, blank=True)
	death_date = models.CharField(max_length=200, blank=True)
	gender = models.CharField(max_length=200, blank=True)
	date_place_lived = models.ManyToManyField('AuthorPlaceDateLived', blank=True)

	@property
	def popupcontent(self):
		return '{} {} {} {} {}'.format(self.name, self.abstract, self.birth_date, self.death_date, self.gender)

	# Link needed?
	def __str__(self):
		return self.name


class Text(models.Model):
	title = models.CharField(max_length=200)
	name_eng = models.CharField(max_length=200, blank=True)
	tags = models.ManyToManyField(Tag)
	language = models.ManyToManyField(BooksLanguage, blank=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
	translator = models.ForeignKey('Translator', on_delete=models.CASCADE, blank=True, null=True)
	arlima_link = models.CharField(max_length=200, blank=True)
	me_compendium_link = models.CharField(max_length=200, blank=True)
	ihrt_link = models.CharField(max_length=200, blank=True)
	def __str__(self):
		return self.title

class Location(models.Model):
	image = models.ImageField( null=True, blank=True)
	geom = models.PointField(null=True, blank=True)
	name =  models.CharField(max_length=200, blank=True)
	City =  models.CharField(max_length=200)
	Country =  models.CharField(max_length=200)

	@property
	def popupcontent(self):
		str = ""
		a = OwnerPlaceDateLived.objects.filter(the_place=self)
		if len(a) == 0:
			return "This isn't supposed to be here, please let us know if you see this."
		for owner_loc in a:
			b = (Owner.objects.filter(owner_location=owner_loc))
			if len(b) != 0:
				str =  str + '<a href="owners/{}/">{}</a>, {} <br>'.format(b[0].name, b[0].name, owner_loc.date_at_location)
		return '<strong>{}, {}</strong><br>{}'.format(self.City, self.Country, str)

	def __str__(self):
		return self.name

class Owner(models.Model):
	image = models.ImageField(null=True, blank=True)
	image_citation = models.CharField(max_length=500, blank=True, null=True)
	name = models.CharField(max_length=200)
	motto = models.CharField(max_length=200, blank=True, null=True)
	birth_year = models.CharField(max_length=200, blank=True, null=True)
	death_year = models.CharField(max_length=200, blank=True, null=True)
	titles = models.CharField(max_length=200, blank=True, null=True)
	Female = 'Female'
	Male = 'Male'
	gen_choices = [(Female, "Female"),(Male, "Male")]
	gender = models.CharField(max_length=9, choices=gen_choices, default='Female')
	symbol = models.CharField("Symbol(s)", max_length=200, blank=True, null=True)
	book_date = models.ManyToManyField('DateOwned', blank=True)
	owner_location = models.ManyToManyField('OwnerPlaceDateLived', blank=True)
	relation = models.ManyToManyField('Relative', blank=True, verbose_name='Relatives')
	@property
	def popupcontent(self):
		t = self.owner_location.all()
		if len(t) == 0:
			date = "no date"
			place = "No location"
		else:
			date = t[0].date_at_location
			place = t[0].the_place
		return '<strong>{}</strong><p>in {} {}</p>'.format(self.name, place, date)
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

	inscription = 'Inscription'
	patron_portrait = 'Patron Portrait'
	inventory = 'Inventory'
	archival_mention = 'Archival Mention'
	arms = 'Arms'
	will = 'Will'
	other = 'Other'
	type_choices = [(inscription, "Inscription"), (patron_portrait, "Patron Portrait"), (inventory,"Inventory"), (archival_mention, "Archival Mention"), (arms, "Arms"), (will, "Will"), (other, "Other")]
	evidence = models.CharField(max_length=40, choices=type_choices, default='Inscription')

	def date_range(self):
		from datetime import datetime, timedelta
		dates = self.dateowned.split('-')
		print(self.dateowned)
		print(dates)
		month = "January"
		day = 1
		year = 1350
		final = []
		chop = 0
		firstDate = True
		if len(dates[0]) == 0 and len(dates[1]) == 0:
			# If we just get a dash return the full possible date range
			x = []
			x.append(datetime.datetime(1350, 1, 1))
			x.append(datetime.datetime(1500, 12, 31))
			return x
		# For start date and finish date
		for date in dates:
			print(date)
			date = date.lstrip()
			date = date.rstrip()
			# How we want to organize uncertain dates
			if date.find('?') != -1 and len(date) < 2:
				# When we get just a "?"
				if firstDate:
					date = "1350"
				else:
					date = "1500"
			if date.find('?') != -1:
				# Maybe add an uncertainty factor to this
				# If we get a date with a ? i.e. "1460?"
				date = date.replace("?", "")
			if "c." in date:
				# Maybe do a +/- operation to just get a range straight off the bat
				# For now just chop
				date = date.replace("c. ", "")
				date = date.replace("c.", "")
			if date.find('/') != -1:
				# For now just take the earlier date... maybe change this
				chop = date.index('/')
				if firstDate:
					# Take the earlier date- this is most/all of the dates we encounter
					date = date[:chop]
				else:
					# Take the later date when its the second date- widest range
					# (Makes "1450/60 "into "1460")
					date = date[:chop-2]+date[chop+1:]
			# We now have a certain date
			date = date.split(' ')
			print("AHHH DATE")
			print(date)
			if len(date[0]) < 3:
				# e.g. 15 December 1443
				day = date[0]
				month = date[1]
				year = date[2]
			elif len(date) == 2:
				# e.g. December 1443
				month = date[0]
				year = date[1]
			else:
				# e.g. 1443
				year = date[0]

			stringIt = str(year) + "-" + month + "-" + str(day)
			#print(StringIt)
			final.append(datetime.strptime(stringIt, "%Y-%B-%d"))
			firstDate = False
			print(final)

		if len(final) == 1:
		# If we are only given one date (e.g. 1433), how far do we stretch the window (currently 2 yrs)
			final.append(final[0] + timedelta(days=731))
			final[0] = final[0] - timedelta(days=730)
		return final
	class Meta:
		verbose_name = 'Date owned'
		verbose_name_plural = 'Dates Book Owned'

	def __str__(self):
		return self.book_owned.shelfmark + ", " + self.dateowned
		#return self.dateowned

class AuthorPlaceDateLived(models.Model):
	place_date_lived = models.CharField(max_length=200, null=True)
	place = models.PointField(null=True, blank=True)
	place_name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.place_date_lived

	class Meta:
		verbose_name = 'Author Location'

class OwnerPlaceDateLived(models.Model):
	geom = models.PointField(null=True, blank=True)
	the_place = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
	date_at_location = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.the_place.name + ", " + self.date_at_location

	def date_range(self):
		from datetime import datetime, timedelta
		dates = self.date_at_location.split('-')
		print(dates)
		month = "January"
		day = 1
		year = 1350
		final = []
		chop = 0
		firstDate = True
		if len(dates[0]) == 0 and len(dates[1]) == 0:
			# If we just get a dash return the full possible date range
			x = []
			x.append(datetime.datetime(1350, 1, 1))
			x.append(datetime.datetime(1500, 12, 31))
			return x
		# For start date and finish date
		for date in dates:
			print(date)
			date = date.lstrip()
			date = date.rstrip()
			# How we want to organize uncertain dates
			if date.find('?') != -1 and len(date) < 2:
				# When we get just a "?"
				if firstDate:
					date = "1350"
				else:
					date = "1500"
			if date.find('?') != -1:
				# Maybe add an uncertainty factor to this
				# If we get a date with a ? i.e. "1460?"
				date = date.replace("?", "")
			if "c." in date:
				# Maybe do a +/- operation to just get a range straight off the bat
				# For now just chop
				date = date.replace("c. ", "")
				date = date.replace("c.", "")
			if date.find('/') != -1:
				# For now just take the earlier date... maybe change this
				chop = date.index('/')
				if firstDate:
					# Take the earlier date- this is most/all of the dates we encounter
					date = date[:chop]
				else:
					# Take the later date when its the second date- widest range
					# (Makes "1450/60 "into "1460")
					date = date[:chop-2]+date[chop+1:]
			# We now have a certain date
			date = date.split(' ')
			print("AHHH DATE")
			print(date)
			if len(date[0]) < 3:
				# e.g. 15 December 1443
				day = date[0]
				month = date[1]
				year = date[2]
			elif len(date) == 2:
				# e.g. December 1443
				month = date[0]
				year = date[1]
			else:
				# e.g. 1443
				year = date[0]

			stringIt = str(year) + "-" + month + "-" + str(day)
			#print(StringIt)
			final.append(datetime.strptime(stringIt, "%Y-%B-%d"))
			firstDate = False
			print(final)

		if len(final) == 1:
		# If we are only given one date (e.g. 1433), how far do we stretch the window (currently to the end of the year)
			final.append(final[0]+ timedelta(days=364))
		return final

	@property
	def popupcontent(self):
		owner = Owner.objects.get(owner_location=self)
		str = '<a href="owners/{}/">{}</a>, {} <br>'.format(owner.name, owner.name, self.date_at_location)
		return '<strong>{}, {}</strong><br>{}'.format(self.the_place.City, self.the_place.Country, str)

	class Meta:
		verbose_name = 'Owner Location'

class Bibliography(models.Model):
	author_date = models.CharField(max_length=200)
	source = models.CharField(max_length=10000)

	def __str__(self):
		return self.author_date
	class Meta:
		verbose_name_plural = 'Bibliographies'

class Relative(models.Model):
	person = models.ForeignKey(Owner,  on_delete=models.SET_NULL, null=True)
	Father = 'Father'
	Mother = 'Mother'
	Spouse = 'Spouse'
	Son = 'Son'
	Daughter = 'Daughter'
	Other = 'Other'
	Brother = 'Brother'
	Sister = 'Sister'
	Aunt = 'Aunt'
	Uncle = 'Uncle'
	Cousin = 'Cousin'
	DiL = 'Daughter-in-law'
	SiL = 'Son-in-law'
	MiL = 'Mother-in-law'
	FiL = 'Father-in-law'
	SiL = 'Sister-in-law'
	BiL = 'Brother-in-law'
	God_son = 'God-son'
	God_parent = 'God-parent'
	God_daughter = 'God-Daughter'
	rel_choices = [(Father, "Father"),(Mother, "Mother"), (Spouse, "Spouse"), (Son, "Son"), (Daughter, 'Daughter'), (Brother, 'Brother'),(Sister, 'Sister'),(Aunt, 'Aunt'),(Uncle, 'Uncle'),(Cousin, 'Cousin'),(DiL, 'Daughter-in-law'),(SiL, 'Son-in-Law'),(MiL, 'Mother-in-law'), (FiL, 'Father-in-law'), (SiL, 'Sister-in-law'), (BiL, 'Brother-in-law'), (God_son, 'God-son'), (God_parent, 'God-parent'), (God_parent, 'God-parent'), (God_daughter, 'God-Daughter')]
	relation = models.CharField(max_length=20, choices=rel_choices, default='Father')

	def __str__(self):
                return self.person.name + ", " + self.relation

class Translator(models.Model):
	name = models.CharField(max_length=200)
	arlima = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
                return self.name

class BookLocation(models.Model):
	geom = models.PointField(null=True, blank=True)
	book_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
	date = models.CharField(max_length=200, null=True)
	book_shelfmark = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
	owner_at_time = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.book_shelfmark.shelfmark + ", " + self.book_location.City + ", " + self.date

	@property
	def popupcontent(self):
		book = self.book_shelfmark
		str = '<a href="http://booksofduchesses.com/books/{}">{}</a>, owned by <a href="http://booksofduchesses.com/owners/{}/">{}</a> ({}) <br>'.format(book.shelfmark, book.shelfmark, self.owner_at_time, self.owner_at_time, self.date)
		return '<strong>{}, {}</strong><br>{}'.format(self.book_location.City, self.book_location.Country, str)

	def date_range(self):
		from datetime import datetime, timedelta
		dates = self.date.split('-')
		print(dates)
		month = "January"
		day = 1
		year = 1350
		final = []
		chop = 0
		firstDate = True
		if len(dates[0]) == 0 and len(dates[1]) == 0:
			# If we just get a dash return the full possible date range
			x = []
			x.append(datetime.datetime(1350, 1, 1))
			x.append(datetime.datetime(1500, 12, 31))
			return x
		# For start date and finish date
		for date in dates:
			print(date)
			date = date.lstrip()
			date = date.rstrip()
			# How we want to organize uncertain dates
			if date.find('?') != -1 and len(date) < 2:
				# When we get just a "?"
				if firstDate:
					date = "1350"
				else:
					date = "1500"
			if date.find('?') != -1:
				# Maybe add an uncertainty factor to this
				# If we get a date with a ? i.e. "1460?"
				date = date.replace("?", "")
			if "c." in date:
				# Maybe do a +/- operation to just get a range straight off the bat
				# For now just chop
				date = date.replace("c. ", "")
				date = date.replace("c.", "")
			if date.find('/') != -1:
				# For now just take the earlier date... maybe change this
				chop = date.index('/')
				if firstDate:
					# Take the earlier date- this is most/all of the dates we encounter
					date = date[:chop]
				else:
					# Take the later date when its the second date- widest range
					# (Makes "1450/60 "into "1460")
					date = date[:chop-2]+date[chop+1:]
			# We now have a certain date
			date = date.split(' ')
			print("AHHH DATE")
			print(date)
			if len(date[0]) < 3:
				# e.g. 15 December 1443
				day = date[0]
				month = date[1]
				year = date[2]
			elif len(date) == 2:
				# e.g. December 1443
				month = date[0]
				year = date[1]
			else:
				# e.g. 1443
				year = date[0]

			stringIt = str(year) + "-" + month + "-" + str(day)
			#print(StringIt)
			final.append(datetime.strptime(stringIt, "%Y-%B-%d"))
			firstDate = False
			print(final)

		if len(final) == 1:
		# If we are only given one date (e.g. 1433), how far do we stretch the window (currently to the end of the year)
			final.append(final[0]+ timedelta(days=364))
		return final
