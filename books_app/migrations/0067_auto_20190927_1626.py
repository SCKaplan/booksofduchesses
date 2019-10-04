# Generated by Django 2.2.2 on 2019-09-27 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0066_auto_20190927_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='authors',
            field=models.ManyToManyField(blank=True, to='books_app.Author'),
        ),
        migrations.AlterField(
            model_name='text',
            name='translators',
            field=models.ManyToManyField(blank=True, to='books_app.Translator'),
        ),
    ]