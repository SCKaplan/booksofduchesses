# Generated by Django 2.2.2 on 2019-07-16 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0051_remove_text_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='text',
            field=models.ManyToManyField(blank=True, to='books_app.Text', verbose_name='Text(s)'),
        ),
    ]