from django.db import models
from django import forms

# Create your models here.
class Settings(models.Model):
    kmallowence = models.IntegerField(max_length=3)     #30 cent
    dailyallowence = models.DecimalField()              #14 Euro
    fulldayallowence = models.DecimalField()            #28 Euro
    dailycompensation = models.DecimalField()           #80 Euro
    bfreduction = models.DecimalField()                 #5,60 Euro


class Referee(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    houseno = models.IntegerField(max_length=5)
    pid = models.IntegerField(max_length=5)
    city = models.CharField(max_length=50)
    IBAN = models.CharField(max_length=22)


class Club(models.Model):
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    houseno = models.IntegerField(max_length=5)
    pid = models.IntegerField(max_length=5)
    city = models.CharField(max_length=50)


class Event(models.Model):
    referee = models.ForeignKey('expenses.Referee', on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=100)
    startdate = models.DateField(editable=True)
    enddate = models.DateField(editable=True)
    noofnights = models.IntegerField(max_length=3)
    noofbreakfasts = models.IntegerField(max_length=3)
    status = models.BooleanField(default=False)        #sent = True


class Dailytravel(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='dailytravels')
    date = models.DateField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    type = models.CharField(max_length=30)  # PKW, Flugzeug, Bahn
    km = models.IntegerField()
    comment = models.CharField(max_length=30)


class Receipt(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='receipts')
    file = forms.FileField()








