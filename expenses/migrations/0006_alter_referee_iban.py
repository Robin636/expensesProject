# Generated by Django 5.0 on 2023-12-23 16:03

import localflavor.generic.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0005_referee_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referee',
            name='IBAN',
            field=localflavor.generic.models.IBANField(include_countries=('AD', 'AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GB', 'GI', 'GR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MC', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'SM', 'VA'), max_length=34, use_nordea_extensions=False),
        ),
    ]
