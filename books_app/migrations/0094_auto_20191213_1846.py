# Generated by Django 2.2.2 on 2019-12-13 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0093_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='name',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='about',
            name='about',
            field=models.TextField(blank=True, help_text='Modify this field. DO NOT CREATE ANOTHER MODEL'),
        ),
    ]