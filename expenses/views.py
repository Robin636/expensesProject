from django.shortcuts import render, get_object_or_404, redirect

from expenses.models import Setting, Club, Game, Event, Dailytravel, Receipt

from expenses.models import Referee

from expenses.forms import EventForm, RefereeForm

from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

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


class RefereeCreateView(CreateView):
  model = Referee
  form_class = RefereeForm
  template_name = "expenses/referee_form.html"
  success_url = reverse_lazy('expenses:referee_detail')

  def form_valid(self, form):
    form.author = self.request.user.id

    ref_new = form.save(commit=False)
    ref_new.save()

    return super(RefereeCreateView, self).form_valid(form)


class RefereeDetailView(DetailView):
  model = Referee
  template_name = "expenses/referee_detail.html"
  success_url = reverse_lazy('expenses:referee')


class RefereeUpdateView(LoginRequiredMixin, UpdateView):
  model = Referee
  form_class = RefereeForm
  #template_name = 'expenses/referee_detail.html'
  success_url = reverse_lazy('expenses:referee')


  def form_valid(self, form):
    referee_new = form.save(commit=False)
    referee_new.id = 0
    referee_new.save()

    return super(RefereeUpdateView, self).form_valid(form)


# def __init__(self, *args, **kwargs):
#   super(RefereeCreateView, self).__init__(*args, **kwargs)
#   self.fields['author'].widget.attrs['disabled'] = True


pass


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




