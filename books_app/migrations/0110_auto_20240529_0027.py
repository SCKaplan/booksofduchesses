# Generated by Django 2.2.24 on 2024-05-29 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0109_auto_20240529_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='editor_credit',
            field=models.TextField(blank=True, verbose_name='Editor Credit'),
        ),
        migrations.AddField(
            model_name='owner',
            name='editor_credit',
            field=models.TextField(blank=True, verbose_name='Editor Credit'),
        ),
    ]