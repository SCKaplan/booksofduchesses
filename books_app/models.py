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





# class DateOwned(MultiValueField):
# 	def __init__(self, **kwargs):
# 		# Define one message for all fields.
# 		error_messages = {
#     		'incomplete': 'Enter an owner and a date of ownership.',
# 			}
# 		# Or define a different message for each field.
# 		fields = (
# 		    ManyToManyField('Owner'),
# 		    DateTimeField(),
# 		)
# 		super().__init__(
# 		    fields=fields,
# 		    require_all_fields=False, **kwargs
# 		)











# class Text(models.Model):
#     title = models.CharField(max_length=30)
#     english_title = models.CharField(max_length=30)
#     language = models.CharField(max_length=30)
#     tags = models.ManyToManyField(Tag)
#
#
# class TextinBook(models.Model):
#     text = models.ForeignKey(Text, on_delete=models.CASCADE)
#     book = models.ManyToManyField(Tag)
#     page_range = models.CharField(max_length=30)
#
#
# class Person(models.Model):
# 	book_owner = models.CharField(max_length=200)
# 	text_author = models.CharField(max_length=200)
# 	book_author = models.CharField(max_length=200)
