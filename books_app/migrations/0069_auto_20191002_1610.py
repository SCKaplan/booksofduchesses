# Generated by Django 2.2.2 on 2019-10-02 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0068_auto_20190930_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='estc_link',
            field=models.CharField(blank=True, max_length=800, verbose_name='ESTC Link'),
        ),
        migrations.AlterField(
            model_name='text',
            name='ihrt_link',
            field=models.CharField(blank=True, max_length=800),
        ),
        migrations.AlterField(
            model_name='text',
            name='me_compendium_link',
            field=models.CharField(blank=True, max_length=200, verbose_name='ME Compendium Link'),
        ),
    ]
