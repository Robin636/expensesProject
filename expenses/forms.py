from django import forms
from expenses.models import Club, Dailytravel, Event, Game, Receipt, Referee, Setting
from django.forms import Textarea, RadioSelect
from django.core import validators
from django.contrib.auth.models import User


class EventForm(forms.ModelForm):
  required_css_class = 'required'

  class Meta():
    model = Event
    # exclude = ('noofnights', 'noofbreakfasts', 'status')
    # fields = ('name',)
    fields = ('name','game', 'club', 'startdate', 'enddate')
    widgets = {
      'name': Textarea(attrs={'cols': 40, 'rows': 1, 'autofocus': True}),
    }


class RefereeForm(forms.ModelForm):
  required_css_class = 'required'

  firstname = forms.CharField(max_length=30, label='Vorname')
  lastname = forms.CharField(max_length=30, label='Nachname')
  street = forms.CharField(max_length=40, label='Straße')
  houseno = forms.CharField(max_length=30, label='Hausnummer')
  pid = forms.IntegerField(label='Postleitzahl')
  city = forms.CharField(max_length=30, label='Stadt')
  telefon = forms.CharField(max_length=30, required=False, label='Telefonnummer')
  IBAN = forms.CharField(min_length=22, max_length=34, label='IBAN')
  BIC = forms.CharField(max_length=12, label='BIC')
  nameBank = forms.CharField(max_length=30, label='Name der Bank')

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




