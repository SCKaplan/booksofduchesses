# Generated by Django 2.2.2 on 2019-07-10 18:44

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0046_auto_20190708_1805'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authorplacedatelived',
            options={'verbose_name': 'Author Location'},
        ),
        migrations.AlterModelOptions(
            name='ownerplacedatelived',
            options={'verbose_name': 'Owner Location'},
        ),
        migrations.CreateModel(
            name='BookLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('date', models.CharField(max_length=200, null=True)),
                ('book_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books_app.Location')),
            ],
        ),
    ]
