# Generated by Django 2.2.2 on 2019-06-26 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0037_auto_20190626_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='geom',
        ),
    ]