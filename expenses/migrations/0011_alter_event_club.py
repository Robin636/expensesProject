# Generated by Django 5.0 on 2023-12-26 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0010_alter_dailytravel_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='events_club', to='expenses.club'),
        ),
    ]
