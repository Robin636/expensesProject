# Generated by Django 5.0 on 2023-12-26 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0007_event_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['startdate']},
        ),
        migrations.RemoveField(
            model_name='event',
            name='author',
        ),
        migrations.AddField(
            model_name='event',
            name='referee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='events_referee', to='expenses.referee'),
            preserve_default=False,
        ),
    ]
