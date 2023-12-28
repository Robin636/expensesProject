from django.db import models
from django import forms
from django.urls import reverse
from localflavor.generic.models import IBANField
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES

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


class Dailytravel(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='events_dailytravel')
    date = models.DateField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    type = models.CharField(max_length=30)  # PKW, Flugzeug, Bahn
    km = models.IntegerField()
    comment = models.CharField(max_length=30)

    def __str__(self):
        return self.date



class Event(models.Model):
    referee = models.ForeignKey('expenses.Referee', on_delete=models.DO_NOTHING, related_name='events_referee')
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    noofnights = models.IntegerField()
    noofbreakfasts = models.IntegerField()
    status = models.BooleanField(default=False)  # sent = True
    game = models.ForeignKey('expenses.Game', on_delete=models.DO_NOTHING, related_name='events_game')
    club = models.ForeignKey('expenses.Club', on_delete=models.DO_NOTHING, related_name='events_club')

    class Meta:
        ordering = ['startdate']


    def get_absolute_url(self):
        return reverse('expenses:referee', args=[str(self.id)])

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=50)
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
    street = models.CharField(max_length=50)
    houseno = models.CharField(max_length=50)
    pid = models.IntegerField()
    city = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20)
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


class Setting(models.Model):
    kmallowence = models.DecimalField(max_digits=3, decimal_places=2)                #30 cent
    dailyallowence = models.DecimalField(max_digits=2, decimal_places=0)              #14 Euro
    fulldayallowence = models.DecimalField(max_digits=2, decimal_places=0)            #28 Euro
    dailycompensation = models.DecimalField(max_digits=3, decimal_places=0)           #80 Euro
    bfreduction = models.DecimalField(max_digits=4, decimal_places=2)                 #5,60 Euro

    def __str__(self):
        return self.id





















