from django.shortcuts import render, get_object_or_404, redirect
from expenses.models import Setting, Referee, Club, Game, Event, Dailytravel, Receipt

#from expenses.forms import ChapForm, PairForm, CallForm, SettingsForm

from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.models import User
import random, os


def index(request):
  return render(request, 'base.html')


class AboutView(TemplateView):
  template_name = 'expenses/about.html'

class EventListView(ListView):
  template_name = "expenses/event_list.html"
  model = Game
  context_object_name = 'game'

  @method_decorator(login_required)
  def for_dec(self, request):
    pass

class DailytravelListView(ListView):
  template_name = "expenses/dt_new.html"
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

