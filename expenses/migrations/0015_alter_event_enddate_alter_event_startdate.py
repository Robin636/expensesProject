# Generated by Django 5.0 on 2024-01-17 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0014_alter_event_enddate_alter_event_noofbreakfasts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='enddate',
            field=models.DateTimeField(null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='event',
            name='startdate',
            field=models.DateTimeField(null=True, verbose_name='date published'),
        ),
    ]