# Generated by Django 2.2.2 on 2019-06-12 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0018_auto_20190612_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='owner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
