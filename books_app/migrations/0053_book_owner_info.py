# Generated by Django 2.2.2 on 2019-07-17 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("books_app", "0052_book_text")]

    operations = [
        migrations.AddField(
            model_name="book",
            name="owner_info",
            field=models.ManyToManyField(
                blank=True,
                to="books_app.DateOwned",
                verbose_name="Ownership Information/History",
            ),
        )
    ]
