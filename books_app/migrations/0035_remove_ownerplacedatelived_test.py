# Generated by Django 2.2.2 on 2019-06-20 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0034_auto_20190620_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ownerplacedatelived',
            name='test',
        ),
    ]
