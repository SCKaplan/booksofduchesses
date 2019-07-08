# Generated by Django 2.2.2 on 2019-07-01 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0040_auto_20190701_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='owner',
            name='image_citation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
