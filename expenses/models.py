from django.db import models
from django import forms


# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    houseno = models.IntegerField()
    pid = models.IntegerField()
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50, default='Bayern')

    def __str__(self):
        return '(id: ' + str(self.id) + ') ' + self.name


class Dailytravel(models.Model):
    date = models.DateField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    type = models.CharField(max_length=30)  # PKW, Flugzeug, Bahn
    km = models.IntegerField()
    comment = models.CharField(max_length=30)
    event = models.ForeignKey('expenses.Event', on_delete=models.DO_NOTHING, related_name='dailytravels')


class Event(models.Model):
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    noofnights = models.IntegerField()
    noofbreakfasts = models.IntegerField()
    status = models.BooleanField(default=False)  # sent = True
    game = models.ForeignKey('expenses.Game', on_delete=models.DO_NOTHING, related_name='events')


class Game(models.Model):
    name = models.CharField(max_length=50)
    AK = models.CharField(max_length=20)
    club = models.ForeignKey('expenses.Club', on_delete=models.CASCADE, related_name='games')

    def __str__(self):
        return '(id: ' + str(self.id) + ') ' + self.name + ' ' + self.AK

class Receipt(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='receipts')
    file = forms.FileField()


class Referee(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    houseno = models.IntegerField()
    pid = models.IntegerField()
    city = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20, default='0')
    IBAN = models.CharField(max_length=22)
    BIC = models.CharField(max_length=12, default='BIC')
    nameBank = models.CharField(max_length=30, default='Bankname')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return '(id: ' + str(self.id) + ') ' + self.lastname + ' ' + self.firstname


class Setting(models.Model):
    kmallowence = models.DecimalField(max_digits=3, decimal_places=2)                #30 cent
    dailyallowence = models.DecimalField(max_digits=2, decimal_places=0)              #14 Euro
    fulldayallowence = models.DecimalField(max_digits=2, decimal_places=0)            #28 Euro
    dailycompensation = models.DecimalField(max_digits=3, decimal_places=0)           #80 Euro
    bfreduction = models.DecimalField(max_digits=4, decimal_places=2)                 #5,60 Euro





















