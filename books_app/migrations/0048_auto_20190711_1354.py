# Generated by Django 2.2.2 on 2019-07-11 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0047_auto_20190710_1844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_movements',
        ),
        migrations.AddField(
            model_name='book',
            name='book_location',
            field=models.ManyToManyField(blank=True, to='books_app.BookLocation'),
        ),
    ]
