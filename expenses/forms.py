import bootstrap_datepicker_plus
from django import forms
from expenses.models import Club, Travel, Event, Game, Receipt, Referee, Rates, Days, UploadedFile
from django.forms import Textarea, RadioSelect, DateInput
from django.core import validators
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from crispy_forms.helper import FormHelper

# from django.forms import fields
# import datetime
# import time

class TravelForm(forms.ModelForm):
  required_css_class = 'required'

  class Meta:
    model = Travel
    fields = ['traveldate', 'starttime', 'startlocation', 'endtime', 'endlocation', 'type', 'km', 'comment']
    widgets={
      'traveldate': DatePickerInput(),
      'starttime': TimePickerInput(),
      'endtime': TimePickerInput(),
    }
    type = forms.ChoiceField(label="Art", choices=[('K', 'KFZ'), ('F', 'Flug'), ('Z', 'Zug')])
    km = forms.IntegerField(label="Gefahrene km")
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':20,}))


class DaysForm(forms.ModelForm):
  required_css_class = 'required'
  class Meta:
    model = Days
    fields = ['iNOfOneDayTravel', 'iNOfMoreDaysTravel', 'iNOfDaysBetween', 'iNOfTravelDays', 'iNOfNights', 'cComment']
    widgets = {
      'cComment': forms.Textarea(attrs={'rows':5, 'cols':20,}),
    }
    rates_list = Rates.objects.all()
    rates = rates_list[0] # nur eine Zeile/Object Setting


class EventForm(forms.ModelForm):
  required_css_class = 'required'

  class Meta:
    model = Event
    fields = ('name', 'game', 'club', 'startdate', 'enddate')
    widgets = {
      'startdate': DatePickerInput(),
      'enddate': DatePickerInput(),
    }
    labels = {'name':'Name', 'game':'Wettspiel', 'club':'Golfclub', 'startdate':'1. Turniertag', 'enddate':'Letzter Turniertag',}

    name = forms.CharField(widget=forms.TextInput(attrs={'cols': 80, 'rows': 10, 'autofocus': True}))


class UploadFileForm(forms.ModelForm):

  class Meta:
    model = UploadedFile
    fields = ('file',)


class RefereeForm(forms.ModelForm):
  required_css_class = 'required'

  firstname = forms.CharField(max_length=30, label='Vorname', widget=forms.Textarea(attrs={'cols':22, 'rows': 1, 'autofocus': True}))
  lastname = forms.CharField(max_length=30, label='Nachname', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  email = forms.EmailField(label='E-Mail', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  street = forms.CharField(max_length=40, label='Straße', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  houseno = forms.CharField(max_length=30, label='Hausnummer', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  pid = forms.IntegerField(label='Postleitzahl', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  city = forms.CharField(max_length=30, label='Stadt', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  telefon = forms.CharField(max_length=30, required=False, label='Telefonnummer', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  mobile = forms.CharField(max_length=30, required=False, label='Mobil',
                            widget=forms.Textarea(attrs={'cols': 22, 'rows': 1}))
  IBAN = forms.CharField(min_length=22, max_length=34, label='IBAN', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  BIC = forms.CharField(max_length=12, label='BIC', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  nameBank = forms.CharField(max_length=30, label='Name der Bank', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))

  class Meta():
    model = Referee
    exclude = ('author',)


  def clean_IBAN(self):
    data = self.cleaned_data['IBAN']
    if len(data) < 22:
      raise ValueError('Bitte 22 Zeichen eingeben')
    return data
