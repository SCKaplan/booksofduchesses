# Generated by Django 2.2.2 on 2019-10-08 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0074_auto_20191008_1420'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='owner',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('tag',)},
        ),
    ]