from django.contrib.gis.db import models
from django.forms import ModelForm
import datetime

def date_ranges(given_dates):
    from datetime import datetime, timedelta
    # Split on the dash into two dates
    if given_dates.find('post-') != -1:
        given_dates = given_dates.replace("post-", "post")
    if given_dates.find('pre-') != -1:
        given_dates = given_dates.replace("pre-", "pre")
    dates = given_dates.split('-')
    # Defaults
    month = "January"
    day = 1
    year = 1350
    final = []
    chop = 0
    firstDate = True
    if len(dates[0]) == 0 and len(dates[1]) == 0:
        # If we just get a dash return the full possible date range
        x = []
        x.append(datetime(1350, 1, 1))
        x.append(datetime(1500, 12, 31))
        return x
    # For start date and finish date
    for date in dates:
        # Take off white space
        uncertain = False
        date = date.lstrip()
        date = date.rstrip()
        # How we want to organize uncertain dates
        if (date.find('?') != -1 and len(date) < 2) or date.find('???') != -1:
        	# When we get just a "?"
        	if firstDate:
        		date = "1300"
        	else:
        		date = "1600"
        if date.find('?') != -1 and date.find('??') == -1:
        	# Maybe add an uncertainty factor to this
        	# If we get a date with a ? i.e. "1460?"
        	date = date.replace("?", "")
        	uncertain = True
        if date.find('post') != -1:
        	if firstDate:
        		date = date.replace("post", "")
        	else:
        		date = "1500"
        if date.find('pre') != -1:
                              if firstDate:
                                      date = "1350"
                              else:
                                      date = date.replace("pre", "")
        if date.find('??') != -1:
        	if firstDate:
        		date = date.replace("??", "00")
        	else:
        		date = date.replace("??", "99")
        if "c." in date:
        	# 'c. 1450'
        	# Maybe do a +/- operation to just get a range straight off the bat
        	# For now just get rid of the c.
        	date = date.replace("c. ", "")
        	date = date.replace("c.", "")
        if date.find('/') != -1:
        	chop = date.index('/')
        	if firstDate:
        		# Take the earlier date- this is most/all of the dates we encounter
        		date = date[:chop]
        	else:
        		# Take the later date when its the second date- widest range
        		# (Makes "1450/60 "into "1460")
        		#date = date[:chop-2]+date[chop+1:]
        		date = date[chop+1:]
        # We now have a certain date (no c., ?, /, etc.) we can format it for datetime
        date = date.split(' ')
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
		# Some shit going on here with spaces/tabs
        	if len(date[0]) == 3 and firstDate:
        		date[0] = date[0] + ""  + "0"
        	if len(date[0]) == 3 and not firstDate:
        		date[0] = date[0] + ""  + "9"
        	# e.g. 1443
        	year = date[0]
        stringIt = str(year) + "-" + month + "-" + str(day)
        # format for adding a datetime from a string
        toAdd = datetime.strptime(stringIt, "%Y-%B-%d")
        if uncertain and firstDate:
            toAdd = toAdd - timedelta(days=1826)
        if uncertain and not firstDate:
            toAdd = toAdd + timedelta(days=1824)
        final.append(toAdd)
        firstDate = False
    # If there is no dash we extend the window to a whole year
    if len(final) == 1:
        final.append(final[0]+ timedelta(days=364))
    return final

class Book(models.Model):
	image = models.ImageField(null=True, blank=True)
	shelfmark = models.CharField(max_length=200)
	about = models.TextField(blank=True, verbose_name="About/Content")
	text = models.ManyToManyField('Text', blank=True, verbose_name="Text(s)")

	type_print = 'Print'
	Manuscript = 'Manuscript'
	type_choices = [(type_print, "Print"),(Manuscript, "Manuscript")]
	type = models.CharField(max_length=30, choices=type_choices, default='Manuscript')

	ex_libris = models.TextField(blank=True) # Hasn't been used yet, but is in AirTable so leaving it here
	date_created= models.CharField(max_length=200, blank=True, null=True)
	catalog_entry = models.CharField(max_length=2000, blank=True)
	digital_version = models.CharField(max_length=200, blank=True)
	scribes = models.ManyToManyField('Scribe', blank=True)
	illuminators = models.ManyToManyField('Illuminator', blank=True)
	printer = models.ManyToManyField('Printer', blank=True, verbose_name="Printer Information")
	# These fields are important for mapping
	book_location = models.ManyToManyField('BookLocation', blank=True) # These are searched in the map
	# Helps us cross reference book ownership, also convenient to display on templates
	owner_info = models.ManyToManyField('DateOwned', blank=True, verbose_name="Ownership Information/History")
	bibliography = models.ManyToManyField('Bibliography', blank=True)
	reviewed = models.BooleanField(null=True, default=False)
	comments = models.TextField(blank=True, verbose_name="User Suggestion Comments")

	def __str__(self):
		return self.shelfmark

class Owner(models.Model):
	image = models.ImageField(null=True, blank=True)
	image_citation = models.CharField(max_length=500, blank=True, null=True)
	bio = models.URLField(null=True, blank=True, max_length=500)
	name = models.CharField(max_length=200)
	titles = models.CharField(max_length=200, blank=True, null=True)
	birth_year = models.CharField(max_length=200, blank=True, null=True)
	death_year = models.CharField(max_length=200, blank=True, null=True)

	Female = 'Female'
	Male = 'Male'
	gen_choices = [(Female, "Female"),(Male, "Male")]
	gender = models.CharField(max_length=9, choices=gen_choices, default='Female')

	motto = models.CharField(max_length=200, blank=True, null=True)
	symbol = models.CharField("Symbol(s)", max_length=200, blank=True, null=True)

	arms = models.ImageField(null=True, blank=True)
	arms_citation = models.CharField(max_length=500, blank=True, null=True)
	signatures = models.ImageField(null=True, blank=True)
	signatures_citation = models.CharField(max_length=500, blank=True, null=True)

	# Helps us cross refernce and useful in templates
	book_date = models.ManyToManyField('DateOwned', blank=True, verbose_name='Instance of Book Ownership')
	# This is the object we search for the map- a date range where an owner was in a location
	owner_location = models.ManyToManyField('OwnerPlaceDateLived', blank=True)
	relation = models.ManyToManyField('Relative', blank=True, verbose_name='Relatives')

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name

# A text can appear in multiple books and a book can have multiple texts, this mostly helps fill out the template
class Text(models.Model):
	title = models.CharField(max_length=200)
	name_eng = models.CharField(max_length=200, blank=True)
	tags = models.ManyToManyField('Tag', blank=True)
	language = models.ManyToManyField('BooksLanguage', blank=True)
	date_composed = models.CharField(max_length=200, blank=True, verbose_name="Date Composed (if known)")
	#author = models.ForeignKey('Author', on_delete=models.CASCADE, blank=True, null=True, related_name='old_author')
	authors = models.ManyToManyField('Author', blank=True)
	#translator = models.ForeignKey('Translator', on_delete=models.CASCADE, blank=True, null=True, related_name='old_translator')
	translators = models.ManyToManyField('Translator', blank=True)
	arlima_link = models.CharField(max_length=200, blank=True)
	me_compendium_link = models.CharField(max_length=200, blank=True, verbose_name="ME Compendium Link")
	ihrt_link = models.CharField(max_length=800, blank=True)
	estc_link = models.CharField(max_length=800, blank=True, verbose_name="ESTC Link")
	ustc_link = models.CharField(max_length=800, blank=True, verbose_name="USTC Link")

	def __str__(self):
		return self.title

# These are the owner related objects we map- first we will find the owners which fit a search criteria in the view,
# then we decide which of these to send to the template based on their date_range()
class OwnerPlaceDateLived(models.Model):
	# This is the field leaflet uses to put pins on the map
	geom = models.PointField(null=True, blank=True)
	# This duplicate exists right now for no reason: but it could be useful for re-doing how popups stack
	the_place = models.ForeignKey('Location', on_delete=models.CASCADE, null=True)
	date_at_location = models.CharField(max_length=200, null=True)

	# Outputs a list of len 2- a range of datetimes from an ambigious string
	def date_range(self):
		return date_ranges(self.date_at_location)

	def __str__(self):
		return self.the_place.name + ", " + self.date_at_location

	@property
	def popupcontent(self):
		# The content that goes in the popup on the map- html formatted
		owner = Owner.objects.get(owner_location=self)
		str = '<a href="https://booksofduchesses.com/owners/{}/" target="_blank">{}</a>, {} <br>'.format(owner.name, owner.name, self.date_at_location)
		return '<strong>{}, {}</strong><br>{}'.format(self.the_place.City, self.the_place.Country, str)

	class Meta:
		verbose_name = 'Owner Location'

# Same concept as OwnerDatePlaceLived, but for books
# Data was originally put in by cross referecing when owners owned books with whether
# their location at that point falls in the book date range. Now is standalone for more additions
class BookLocation(models.Model):
	geom = models.PointField(null=True, blank=True)
	# Duplicate for the same reason as OwnerDatePlaceLived
	book_location = models.ForeignKey('Location', on_delete=models.CASCADE, null=True)
	date = models.CharField(max_length=200, null=True)
	book_shelfmark = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
	owner_at_time = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)

	# Outputs a list of len 2- a range of datetimes from an ambigious string
	def date_range(self):
		return date_ranges(self.date)

	@property
	def popupcontent(self):
		book = self.book_shelfmark
		str = '<a href="http://booksofduchesses.com/books/{}" target="_blank">{}</a>, owned by <a href="http://booksofduchesses.com/owners/{}/" target="_blank">{}</a> ({}) <br>'.format(book.shelfmark, book.shelfmark, self.owner_at_time, self.owner_at_time, self.date)
		return '<strong>{}, {}</strong><br>{}'.format(self.book_location.City, self.book_location.Country, str)

	def __str__(self):
		return self.book_shelfmark.shelfmark + ", " + self.book_location.City + ", " + self.date

# An individual ownership event- catalogs when an owner owned a certain book and some more info
class DateOwned(models.Model):
	book_owned = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
	dateowned = models.CharField(max_length=200, null = True)
	book_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, help_text="If you don't have a known owner for this entry, select No known Owner")
	Conf = 'confirmed'
	Poss = 'possibly'
	conf_choices = [(Conf, "confirmed"),(Poss, "possibly")]
	conf_or_possible = models.CharField(max_length=9, choices=conf_choices, default='confirmed')

	inscription = 'Inscription'
	patron_portrait = 'Patron Portrait'
	inventory = 'Inventory'
	archival_mention = 'Archival Mention'
	arms = 'Arms'
	will = 'Will'
	other = 'Other'

	type_choices = [(inscription, "Inscription"), (patron_portrait, "Patron Portrait"), (inventory,"Inventory"), (archival_mention, "Archival Mention"), (arms, "Arms"), (will, "Will"), (other, "Other")]
	evidence = models.CharField(max_length=40, choices=type_choices, default='Inscription')
	ownership_type = models.ManyToManyField('Evidence')

	# Outputs a list of len 2- a range of datetimes from an ambigious string
	def date_range(self):
		return date_ranges(self.dateowned)

	class Meta:
		verbose_name = 'Date owned'
		verbose_name_plural = 'Dates Book Owned'

	class Meta:
		ordering = ('book_owner',)

	def __str__(self):
		return self.book_owned.shelfmark + ", " + self.book_owner.name + ", " + self.dateowned
		#return self.book_owner.name + ", " + self.dateowned

# Not necesarilly useful or necessary but I'm keeping this around until we figure out stacking on the map
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
				str =  str + '<a  href="https://booksofduchesses.com/owners/{}/" target="_blank" >{}</a>, {} <br>'.format(b[0].name, b[0].name, owner_loc.date_at_location)
		return '<strong>{}, {}</strong><br>{}'.format(self.City, self.Country, str)

	def __str__(self):
		return self.name

# Linked to texts: Author has geo capabilities but these aren't used at the moment
class Author(models.Model):
	name = models.CharField(max_length=200)
	birth_date = models.CharField(max_length=200, blank=True)
	death_date = models.CharField(max_length=200, blank=True)
	link = models.CharField(max_length=1000, blank=True, verbose_name="Further Information (link)")

	Female = 'Female'
	Male = 'Male'
	gen_choices = [(Female, "Female"),(Male, "Male")]
	gender = models.CharField(max_length=9, choices=gen_choices, default='Female')

	image = models.ImageField(null=True, blank=True)
	geom = models.PointField(null=True, blank=True)

	@property
	def popupcontent(self):
		return '<p>Author popup</p>'

	def __str__(self):
		return self.name

# Source reference for book ownership
class Bibliography(models.Model):
	author_date = models.CharField(max_length=200, verbose_name="Author Last Name, Date")
	source = models.CharField(max_length=10000)

	def __str__(self):
		return self.author_date
	class Meta:
		verbose_name_plural = 'Bibliographies'

# Can be used to make something resembling a family tree in the future
class Relative(models.Model):
	person = models.ForeignKey(Owner,  on_delete=models.SET_NULL, null=True)
	# Worth considering whether this should be made its own class instead of the whole massive dropdown
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
	SoniL = 'Son-in-law'
	MiL = 'Mother-in-law'
	FiL = 'Father-in-law'
	SisiL = 'Sister-in-law'
	BiL = 'Brother-in-law'
	God_son = 'God-son'
	God_parent = 'God-parent'
	God_daughter = 'God-Daughter'
	Niece = 'Niece'
	Nephew = 'Nephew'
	Grandmother = 'Grandmother'
	Grandfather = 'Grandfather'
	GreatAunt = 'Great Aunt'
	GreatUncle = 'Great Uncle'
	Granddaughter = 'Granddaughter'
	Grandson = 'Grandson'
	GrandNiece = 'Grand Niece'
	GrandNephew = 'Grand Nephew'
	Other = 'Other'
	rel_choices = [(Father, "Father"), (Mother, "Mother"), (Spouse, "Spouse"), (Son, "Son"), (Daughter, 'Daughter'), (Brother, 'Brother'), (Sister, 'Sister'),\
	(Aunt, 'Aunt'),(Uncle, 'Uncle'),(Cousin, 'Cousin'),(DiL, 'Daughter-in-law'),(SoniL, 'Son-in-Law'), (MiL, 'Mother-in-law'), (FiL, 'Father-in-law'), (SisiL, 'Sister-in-law'),\
	(BiL, 'Brother-in-law'), (God_son, 'God-son'), (God_parent, 'God-parent'), (God_parent, 'God-parent'), (God_daughter, 'God-Daughter'), (Niece, "Niece"),\
	(Nephew, "Nephew"), (Grandmother, "Grandmother"), (Grandfather, "Grandafather"), (GreatAunt, "Great Aunt"), (GreatUncle, "Great Uncle"), \
	(Granddaughter, "Granddaughter"), (Grandson, "Grandson"), (GrandNiece, "Grand Niece"), (GrandNephew, "Grand Nephew"), (Other, 'Other')]
	relation = models.CharField(max_length=40, choices=rel_choices, default='Father')

	def __str__(self):
                return self.person.name + ", " + self.relation

# Linked in Text
class Translator(models.Model):
	name = models.CharField(max_length=200)
	birth_year = models.CharField(max_length=200, blank=True, null=True)
	death_year = models.CharField(max_length=200, blank=True, null=True)

	Female = 'Female'
	Male = 'Male'
	gen_choices = [(Female, "Female"),(Male, "Male")]
	gender = models.CharField(max_length=9, choices=gen_choices, default='Female')

	link = models.CharField(max_length=200, blank=True, null=True, verbose_name="Further Information (link)")
	image = models.ImageField(null=True, blank=True)
	geom = models.PointField(null=True, blank=True)

	def __str__(self):
                return self.name

# Linked in Book
class Illuminator(models.Model):
        name = models.CharField(max_length=200)
        birth_year = models.CharField(max_length=200, blank=True, null=True)
        death_year = models.CharField(max_length=200, blank=True, null=True)

        Female = 'Female'
        Male = 'Male'
        Unknown = 'Unknown'
        gen_choices = [(Female, "Female"),(Male, "Male"),(Unknown, "Unknown")]
        gender = models.CharField(max_length=9, choices=gen_choices, default='Female')

        link = models.CharField(max_length=200, blank=True, null=True, verbose_name="Further Information (link)")
        image = models.ImageField(null=True, blank=True)
        geom = models.PointField(null=True, blank=True)
        def __str__(self):
                return self.name

# Linked in Book
class Scribe(models.Model):
        name = models.CharField(max_length=200)
        birth_year = models.CharField(max_length=200, blank=True, null=True)
        death_year = models.CharField(max_length=200, blank=True, null=True)

        Female = 'Female'
        Male = 'Male'
        Unknown = 'Unknown'
        gen_choices = [(Female, "Female"),(Male, "Male"),(Unknown, "Unknown")]
        gender = models.CharField(max_length=9, choices=gen_choices, default='Female')

        link = models.CharField(max_length=200, blank=True, null=True, verbose_name="Further Information (link)")
        image = models.ImageField(null=True, blank=True)
        geom = models.PointField(null=True, blank=True)

        def __str__(self):
                return self.name

# Texts have descriptive tags- searchable on main page
class Tag(models.Model):
	tag = models.CharField(max_length=200)

	class Meta:
		ordering = ('tag',)

	def __str__(self):
		return self.tag

class BooksLanguage(models.Model):
	books_language = models.CharField(max_length=200)
	#geom = models.PolygonField(null=True, blank=True)
	class Meta:
		verbose_name = 'Language'

	def __str__(self):
		return self.books_language

class OwnershipEvidence(models.Model):
        evidence = models.CharField(max_length=500)

        class Meta:
                verbose_name = 'Evidence'

        def __str__(self):
                return self.evidence

class Printer(models.Model):
        name = models.CharField(max_length=200)
        link = models.CharField(max_length=1000, blank=True, verbose_name="Further Information (link)")
        birth_date = models.CharField(max_length=200, blank=True)
        death_date = models.CharField(max_length=200, blank=True)

        Female = 'Female'
        Male = 'Male'
        gen_choices = [(Female, "Female"),(Male, "Male")]
        gender = models.CharField(max_length=9, choices=gen_choices, default='Female')

        image = models.ImageField(null=True, blank=True)
        geom = models.PointField(null=True, blank=True)

        @property
        def popupcontent(self):
                return '<p>Printer popup</p>'

        def __str__(self):
                return self.name

class Evidence(models.Model):
	Conf = 'Confirmed'
	Poss = 'Possible'
	conf_choices = [(Conf, "Confirmed"),(Poss, "Possible")]
	conf_or_possible = models.CharField(max_length=9, choices=conf_choices, default='confirmed')
	evidence = models.CharField(max_length=200)

	def __str__(self):
		return self.conf_or_possible + ", " + self.evidence


class About(models.Model):
	name = models.CharField(max_length=500, blank=True)
	about = models.TextField(blank=True, help_text="Modify this field. DO NOT CREATE ANOTHER MODEL")

	def __str__(self):
		return self.name



