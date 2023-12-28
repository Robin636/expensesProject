from django.shortcuts import render, get_object_or_404, redirect

from expenses.models import Setting, Club, Game, Event, Dailytravel, Receipt

from expenses.models import Referee

from expenses.forms import EventForm, RefereeForm

from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django import forms
from django.contrib.auth.models import User
import random, os


def index(request):
  return render(request, 'base.html')


class AboutView(TemplateView):
  template_name = 'expenses/about.html'

class EventListView(ListView):
  template_name = "expenses/event_list.html"
  model = Event
  context_object_name = 'event'

  @method_decorator(login_required)
  def for_dec(self, request):
    pass

  # def get_queryset(self):
  #   qs = super().get_queryset()
  #   qs = qs.filter(author_id=self.request.user.id)
  #   qs = qs.order_by("id")
  #   return qs

class EventDetailView(DetailView):
  model = Event
  template_name = "expenses/event_detail.html"


class EventCreateView(LoginRequiredMixin, CreateView):
  model = Event
  form_class = EventForm
  template_name = "expenses/event_form.html"
  success_url = reverse_lazy('expenses:event_list')
  def form_valid(self, form):
    form.instance.author = self.request.user
    #return super(EventCreateView).form_valid(form)

    event_new = form.save(commit=False)
    event_list = Event.objects.all()
    id_list = []
    for item in event_list:
      id_list.append(item.id)

    if len(id_list) > 0:
      id_list.sort()
      id = id_list[-1]
      event_new.id = id + 1
    else:
      event_new.id = 0

    event_new.save()

    return super(EventCreateView, self).form_valid(form)

class EventUpdateView(UpdateView):
  login_url = '/login/'
  model = Event
  form_class = EventForm

  def get_success_url(self):
    return reverse('expenses:event_list')


class EventDeleteView(DeleteView):
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



# def referee_new(request):
#   author = request.user
#   referee_list = Referee.objects.filter(author=author)
#   if referee_list.count() > 0:
#     referee_instance = referee_list.first()
#     form = RefereeForm(request.POST or None, instance=referee_instance)
#   else:
#     form = RefereeForm()
#
#   if request.method == 'POST':
#     if form.is_valid():
#       form.instance.author = request.user
#       ref_new = form.save(commit=False)
#       ref_new.id = 1
#       # allow only one setting
#       ref_new.save()
#
#       return render(request, 'expenses/referee_detail.html')
#
#   else:
#     author = request.user
#     referee_list = Referee.objects.filter(author=author)
#     if referee_list.count() > 0:
#       referee_instance = referee_list.first()
#       form = RefereeForm(request.POST or None, instance=referee_instance)
#     else:
#       form = RefereeForm()
#
#     context = {
#       'form': form,
#     }
#     return render(request, 'expenses/referee_form.html')


class RefereeCreateView(LoginRequiredMixin,CreateView):
  model = Referee
  form_class = RefereeForm
  template_name = "expenses/referee_form.html"
  success_url = reverse_lazy('expenses:referee_settings')



  def form_valid(self, form):
    form.instance.author = self.request.user
    ref_new = form.save(commit=False)
    ref_new.id = 1
    # allow only one setting
    ref_new.save()

    return super(RefereeCreateView, self).form_valid(form)


# class RefereeDetailView(DetailView):
#   model = Referee
#   template_name = "expenses/referee_detail.html"
  # success_url = reverse_lazy('expenses:referee')


# class RefereeUpdateView(LoginRequiredMixin, UpdateView):
#   model = Referee
#   form_class = RefereeForm
#   #template_name = 'expenses/referee_detail.html'
#   success_url = reverse_lazy('expenses:referee')
#
#
#   def form_valid(self, form):
#     referee_new = form.save(commit=False)
#     referee_new.id = 0
#     referee_new.save()
#
#     return super(RefereeUpdateView, self).form_valid(form)


# def __init__(self, *args, **kwargs):
#   super(RefereeCreateView, self).__init__(*args, **kwargs)
#   self.fields['author'].widget.attrs['disabled'] = True





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


#@login_required
# def refereesettings(request):
#   author = request.user.id
#   form = RefereeForm()
#   referee = Referee.objects.update_or_create()
#
#   if request.method == 'POST':
#     form = RefereeForm(request.POST, request.Files)
#     referee = form.save(commit=False)
#     referee.author = request.user
#     referee.save()
#
#   else:
#     author = request.user.id
#     form = RefereeForm()
#     context = {}
#     context['referee'] = referee
#
#     if form.is_valid():
#       Referee = form.save(commit=False)
#     return render(request,'expenses/referee_detail.html')
#
#   return redirect('expenses:event_list')


  # @method_decorator(login_required)
  # def for_dec(self, request):
  #   pass


  #fields = ['firstname', 'lastname', 'street', 'houseno', 'pid', 'city', 'telefon', 'IBAN', 'BIC', 'nameBank', 'author']




