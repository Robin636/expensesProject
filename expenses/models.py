import uuid

from django.db import models
from django import forms
from django.urls import reverse
from django.utils import timezone
from localflavor.generic.models import IBANField
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES

# import datetime
# ISO_date ="2024-02-17"
# default_date = datetime.date.fromisoformat(ISO_date)

# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    houseno = models.IntegerField()
    pid = models.IntegerField()
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50, default='Bayern')

    def __str__(self):
        return self.name
        #return '(id: ' + str(self.id) + ') ' + self.name



TYPE_CHOICES = [('KFZ', 'KFZ'), ('Flug', 'Flug'), ('Zug', 'Zug')]

class Travel(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='events_travel')
    traveldate = models.DateTimeField(null=True)
    starttime = models.TimeField(null=True)
    startlocation = models.CharField(max_length=30, default=" ", blank=False)
    endtime = models.TimeField(null=True)
    duration = models.CharField(max_length=4, default="00:00 ", blank=True)
    endlocation = models.CharField(max_length=30, default=" ", blank=False)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='KFZ')  # PKW, Flugzeug, Bahn
    km = models.IntegerField()
    comment = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ['traveldate']

    def get_absolute_url(self):
        return reverse('expenses:travel_list', kwargs={'pk': self.pk})

    def __str__(self):
        return self.endlocation



INT_CHOICES = [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9')]
class Days(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='events_days')
    iNOfOneDayTravel = models.IntegerField(choices=INT_CHOICES, default=0)
    iNOfMoreDaysTravel = models.IntegerField(choices=INT_CHOICES, default=0)
    iNOfDaysBetween = models.IntegerField(choices=INT_CHOICES, default=0)
    iNOfNights = models.IntegerField(choices=INT_CHOICES, default=0)
    iNOfTravelDays = models.IntegerField(choices=INT_CHOICES, default=0)
    cComment = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('expenses:travel_list', kwargs={'pk': self.pk})

    def __str__(self):
        return self.iNOfTravelDays

def generate_filename(instance, filename):
    event = instance.event
    # ext = filename.split('.')[-1]
    # filename = f'{uuid.uuid4()}.{ext}'
    return f"attachments/{event.id}/{filename}"

class UploadedFile(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='events_uploaded_files')
    # file = models.FileField(upload_to='attachments/')
    file = models.FileField(upload_to=generate_filename)
    file_name = models.CharField(max_length=100, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(default=0)



class Event(models.Model):
    referee = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING, related_name='events_referee')
    name = models.CharField(max_length=100)
    startdate = models.DateTimeField(null=True)
    enddate = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)  # sent = True
    game = models.ForeignKey('expenses.Game', on_delete=models.DO_NOTHING, related_name='events_game')
    club = models.ForeignKey('expenses.Club', on_delete=models.DO_NOTHING, related_name='events_club')
    # attachment = models.FileField(upload_to='attachments/%Y/%m/%d', blank=True)
    # attachment = models.FileField(upload_to='attachments/{%event.pk%}', blank=True)
    attachment = models.FileField(upload_to='attachments/', blank=True)

    class Meta:
        ordering = ['-startdate']

    def get_absolute_url(self):
        return reverse('expenses:travel_list', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name + ' ' + str(self.club)


class Game(models.Model):
    name = models.CharField( max_length=50)
    AK = models.CharField(max_length=20)


    def __str__(self):
        return self.name + ' ' + self.AK
        #return '(id: ' + str(self.id) + ') ' + self.name + ' ' + self.AK


class Receipt(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='events_receipt')
    file = forms.FileField()

    def __str__(self):
        return self.id


class Referee(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(default=' ')
    street = models.CharField(max_length=50)
    houseno = models.CharField(max_length=50)
    pid = models.IntegerField()
    city = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, default=' ', blank=True)
    IBAN = IBANField(include_countries=IBAN_SEPA_COUNTRIES)
    #IBAN = models.CharField(max_length=22)
    BIC = models.CharField(max_length=12, default='BIC')
    nameBank = models.CharField(max_length=30, default='Bankname')

    def get_absolute_url(self):
        #return reverse('expenses:referee_detail', pk=1)
        #return reverse('referee_detail', kwargs={'pk':self.pk})
        return reverse('referee_detail', args=[str(self.id)])

    def __str__(self):
        #return '(id: ' + str(self.id) + ') ' + self.lastname + ' ' + self.firstname
        return self.firstname + ' ' + self.lastname


class Rates(models.Model):
    kmallowence = models.CharField(max_length=5)           #0.30 Euro
    dailyallowence = models.CharField(max_length=5)        #15 Euro
    fulldayallowence = models.CharField(max_length=5)      #30 Euro
    dailycompensation = models.CharField(max_length=5)     #80 Euro
    bfreduction = models.CharField(max_length=5)           #-6 Euro

    def __str__(self):
        return self.id





















