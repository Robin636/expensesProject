from django import forms
from expenses.models import Club, Dailytravel, Event, Game, Receipt, Referee, Setting
from django.forms import Textarea, RadioSelect
from django.core import validators
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper


class EventForm(forms.ModelForm):
  required_css_class = 'required'

  name = forms.CharField(widget=forms.TextInput(attrs={'cols': 80, 'rows': 10, 'autofocus': True}))
  startdate = forms.DateField(widget=DatePickerInput(
    attrs={'class': "event-input"},
    options={
      "format": "DD.MM.YYYY", "showTodayButton": True,
    }
  ))
  enddate = forms.DateField(widget=DatePickerInput(
    attrs={'class': "event-input"},
    options={
      "format": "DD.MM.YYYY", "showTodayButton": True,
    }
  ))

  class Meta:
    model = Event
    fields = ('name', 'game', 'club', 'startdate', 'enddate')
    # widgets = {
    #   "startdate": DatePickerInput(options={'format': 'DD.MM.YYYY'}),
    #   "enddate": DatePickerInput(options={'format': 'DD.MM.YYYY'}),
    # }


class RefereeForm(forms.ModelForm):
  required_css_class = 'required'

  firstname = forms.CharField(max_length=30, label='Vorname', widget=forms.Textarea(attrs={'cols':22, 'rows': 1, 'autofocus': True}))
  lastname = forms.CharField(max_length=30, label='Nachname', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  street = forms.CharField(max_length=40, label='Straße', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  houseno = forms.CharField(max_length=30, label='Hausnummer', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  pid = forms.IntegerField(label='Postleitzahl', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  city = forms.CharField(max_length=30, label='Stadt', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
  telefon = forms.CharField(max_length=30, required=False, label='Telefonnummer', widget=forms.Textarea(attrs={'cols':22, 'rows': 1}))
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



  # class Media:
  #   css = {'all': ('form.css',)}




