# Generated by Django 2.2.2 on 2019-07-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0061_auto_20190725_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='scribes',
            field=models.ManyToManyField(blank=True, to='books_app.Scribe'),
        ),
    ]