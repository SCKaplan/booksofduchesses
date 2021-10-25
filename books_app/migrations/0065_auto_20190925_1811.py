# Generated by Django 2.2.2 on 2019-09-25 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("books_app", "0064_auto_20190731_1801")]

    operations = [
        migrations.AddField(
            model_name="text",
            name="authors",
            field=models.ManyToManyField(to="books_app.Author"),
        ),
        migrations.AlterField(
            model_name="dateowned",
            name="book_owner",
            field=models.ForeignKey(
                help_text="If you don't have a known owner for this entry, select No known Owner",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="books_app.Owner",
            ),
        ),
        migrations.AlterField(
            model_name="text",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="old_author",
                to="books_app.Author",
            ),
        ),
    ]
