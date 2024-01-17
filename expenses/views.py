from django.shortcuts import render, get_object_or_404, redirect

from expenses.models import Setting, Club, Game, Event, Dailytravel, Receipt, Referee
# from expenses.forms import RefereeForm
from expenses.forms import EventForm, RefereeForm

from django.urls import reverse_lazy, reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.utils.decorators import method_decorator

from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from django import forms
#from django.contrib.auth.models import User
#import random, os


def index(request):
  return render(request, 'base.html')


class AboutView(TemplateView):
  template_name = 'expenses/about.html'

class EventCreateView(LoginRequiredMixin, CreateView):
  model = Event
  form_class = EventForm
  template_name = 'expenses/event_form.html'
  success_url = reverse_lazy('expenses:event_list')

  def form_invalid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def form_valid(self, form):
    form.instance.referee = self.request.user.id
    return super().form_valid(form)

class EventListView(LoginRequiredMixin, ListView):
  model = Event
  template_name = ('expenses/event_list.html')
  context_object_name = 'event'
  def get_queryset(self):
    return Event




class EventUpdateView(LoginRequiredMixin, UpdateView):
  model = Event
  # form_class = EventForm
  template_name = "expenses"

  def get_success_url(self):
    return reverse('expenses:event_list')


class EventDeleteView(LoginRequiredMixin, DeleteView):
  model = Event
  success_url = reverse_lazy('expenses:event_list')



def referee_settings(request):
  author = request.user
  referee_list = Referee.objects.filter(author=author)
  if referee_list.count() > 0:
    referee_instance = referee_list.first()
    context = {
      'referee': referee_instance,
    }
    return render(request, 'expenses/referee_detail.html', context)
  else:
    form = RefereeForm()
    context = {
      'form': form,
      'author': request.user
    }
    return render(request, 'expenses/referee_form.html', context)


def referee_update(request, pk):
  referee = get_object_or_404(Referee, pk=pk)
  if request.method == 'POST':
    form = RefereeForm(request.POST, instance=referee)
    if form.is_valid():
      referee = form.save(commit=False)
      referee.author = request.user
      referee.id = 1
      referee.save()
      context = {
        'referee': referee,
      }
      return render(request, 'expenses/referee_detail.html', context)
    else:
      if 'IBAN' in form.errors:
        messages.error(request, 'IBAN nicht korrekt!')

  else:
    form=RefereeForm(instance=referee)
  return render(request, 'expenses/referee_form.html', {'form': form})


# class RefereeCreateView(LoginRequiredMixin,CreateView):
#   model = Referee
#   form_class = RefereeForm
#   template_name = "expenses/referee_form.html"
#   success_url = reverse_lazy('expenses:referee_settings')
#
#   def form_valid(self, form):
#     form.instance.author = self.request.user
#     ref_new = form.save(commit=False)
#     ref_new.id = 1
#     # allow only one setting
#     ref_new.save()
#
#     return super(RefereeCreateView, self).form_valid(form)


class DailytravelListView(ListView):
  template_name = "expenses/event_form.html"
  model = Game
  context_object_name = 'dailytravel'

  @method_decorator(login_required)
  def for_dec(self, request):
    pass

  # def get_queryset(self):
  #   qs = super().get_queryset()
  #   qs = qs.filter(author_id=self.request.user.id)
  #   qs = qs.order_by("id")
  #   return qs





