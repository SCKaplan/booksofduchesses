# Generated by Django 2.2.2 on 2019-10-08 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0073_ownershipevidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relative',
            name='relation',
            field=models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Spouse', 'Spouse'), ('Son', 'Son'), ('Daughter', 'Daughter'), ('Brother', 'Brother'), ('Sister', 'Sister'), ('Aunt', 'Aunt'), ('Uncle', 'Uncle'), ('Cousin', 'Cousin'), ('Daughter-in-law', 'Daughter-in-law'), ('Sister-in-law', 'Son-in-Law'), ('Mother-in-law', 'Mother-in-law'), ('Father-in-law', 'Father-in-law'), ('Sister-in-law', 'Sister-in-law'), ('Brother-in-law', 'Brother-in-law'), ('God-son', 'God-son'), ('God-parent', 'God-parent'), ('God-parent', 'God-parent'), ('God-Daughter', 'God-Daughter'), ('Niece', 'Niece'), ('Nephew', 'Nephew'), ('Other', 'Other')], default='Father', max_length=40),
        ),
    ]