from django.db import models
from django import forms
from django.urls import reverse


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
    game = models.ForeignKey('expenses.Game', on_delete=models.DO_NOTHING, related_name='events_game')
    club = models.ForeignKey('expenses.Club', on_delete=models.CASCADE, related_name='events_club', default=1)

    def get_absolute_url(self):
        return reverse('expenses:referee', args=[str(self.id)])

    def __str__(self):
        return self.name



class Game(models.Model):
    name = models.CharField(max_length=50)
    AK = models.CharField(max_length=20)
    #club = models.ForeignKey('expenses.Club', on_delete=models.CASCADE, related_name='games')

    def __str__(self):
        return self.name + ' ' + self.AK
        #return '(id: ' + str(self.id) + ') ' + self.name + ' ' + self.AK

class Receipt(models.Model):
    event = models.ForeignKey('expenses.Event', on_delete=models.CASCADE, related_name='receipts')
    file = forms.FileField()


class Referee(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    houseno = models.CharField(max_length=50)
    pid = models.IntegerField()
    city = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20, default='0')
    IBAN = models.CharField(max_length=22)
    BIC = models.CharField(max_length=12, default='BIC')
    nameBank = models.CharField(max_length=30, default='Bankname')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('expenses:referee_detail')
        #return reverse('expenses:referee_detail', kwargs={'pk':self.pk})

    def __str__(self):
        #return '(id: ' + str(self.id) + ') ' + self.lastname + ' ' + self.firstname
        return self.firstname + ' ' + self.lastname

# class RefereeForm(forms.Form):
#   required_css_class = 'required'
#   firstname = forms.CharField(max_length=30, label='Vorname')
#   lastname = forms.CharField(max_length=30, label='Nachname')
#   street = forms.CharField(max_length=30, label='Straße')
#   houseno = forms.CharField(max_length=30, label='Hausnummer')
#   pid = forms.IntegerField(label='Postleitzahl')
#   city = forms.CharField(max_length=30, label='Stadt')
#   telefon = forms.CharField(max_length=30, required=False, label='Telefonnummer')
#   IBAN = forms.CharField(max_length=30, label='IBAN')
#
#   class Meta():
#     model = Referee
#     exclude = ('author',)
#
#   class Media:
#     css = {'all': ('form.css',)}


class Setting(models.Model):
    kmallowence = models.DecimalField(max_digits=3, decimal_places=2)                #30 cent
    dailyallowence = models.DecimalField(max_digits=2, decimal_places=0)              #14 Euro
    fulldayallowence = models.DecimalField(max_digits=2, decimal_places=0)            #28 Euro
    dailycompensation = models.DecimalField(max_digits=3, decimal_places=0)           #80 Euro
    bfreduction = models.DecimalField(max_digits=4, decimal_places=2)                 #5,60 Euro





















