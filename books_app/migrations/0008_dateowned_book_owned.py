# Generated by Django 2.2.2 on 2019-06-10 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0007_auto_20190610_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='dateowned',
            name='book_owned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books_app.Book'),
        ),
    ]
