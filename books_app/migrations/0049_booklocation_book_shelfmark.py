# Generated by Django 2.2.2 on 2019-07-11 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0048_auto_20190711_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='booklocation',
            name='book_shelfmark',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books_app.Book'),
        ),
    ]
