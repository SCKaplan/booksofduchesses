# Generated by Django 2.2.2 on 2019-06-26 14:07

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0036_owner_owner_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownerplacedatelived',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
