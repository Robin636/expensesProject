import os

# from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from expenses.models import Rates, Club, Game, Event, Travel, Receipt, Referee, Days, UploadedFile
from expenses.forms import EventForm, RefereeForm, TravelForm, DaysForm, UploadFileForm

from django.urls import reverse_lazy, reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator

from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from datetime import datetime, time
from decimal import Decimal

from django.http import HttpResponse
from .utils import render_to_pdf
from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.core.mail import EmailMessage
# import magic
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def index(request, **kwargs):
  user_id = request.user.id
  # if user_id != None:
  if user_id is not None:
    referee_list = Referee.objects.all().filter(author_id=user_id)
    if referee_list.count() > 0:
      referee = referee_list[0]  # nur eine Zeile/Object pro Referee
      # referee_id = referee.author_id
      event_list = Event.objects.all().filter(referee_id=user_id)
      context = {
        'referee': referee,
        'event_list': event_list,
        'referee_id': referee.id,
      }
      return render(request, 'expenses/event_list.html', context)
    else:
      return render(request, 'base.html')
  else:
    return render(request, 'base.html')


def upload_file(request, pk):
  event = Event.objects.get(pk=pk)
  rates = Rates.objects.get(id=1)
  if request.method == 'POST':

    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      UploadedFile.objects.create(
        file=request.FILES['file'],
        event_id = event.id,
        file_name = form.cleaned_data['file'].name,
        file_size = form.cleaned_data['file'].size,
        uploaded_date= datetime.now(),
      )
    context = create_context_days(event, rates)
    return render(request, 'expenses/travel_list.html', context)
  else:
    form = UploadFileForm()
    context = {
      'event': event,
      'form': form
    }
    return render(request, 'expenses/upload_form.html', context)


def delete_file(request, pk, id):
  event = Event.objects.get(pk=pk)
  file = UploadedFile.objects.get(id=id)
  if request.method == 'GET':
    context = {
      'event': event,
      'file': file,
    }
    return render(request, 'expenses/file_confirm_delete.html',context)
  elif request.method == 'POST':
    # deletes file itself
    path_pk = str(pk)
    path = os.path.join(settings.MEDIA_ROOT, str('attachments/' + path_pk + '/' + file.file_name))
    os.remove(path)
    # deletes from database expenses_uploadedfile
    file.delete()
    messages.success(request, "Anhang wurde gelöscht")

  rates = Rates.objects.get(id=1)
  context = create_context_days(event, rates)
  return render(request, 'expenses/travel_list.html', context)


def event_send(request, pk):
  event = Event.objects.get(pk=pk)
  rates = Rates.objects.get(id=1)

  referee_id = event.referee_id
  referee = Referee.objects.get(author_id=referee_id)
  startdate = event.startdate
  startdate = startdate.strftime('%d.%m.%Y')
  subject = str(event.name) + ': ' + str(event.club) + ' am ' + str(startdate)

  context = create_context_days(event, rates)
  html_message = render_to_string('expenses/travel_pdf.html', context)
  plain_message = strip_tags(html_message)
  from_email = referee.email
  to = settings.EMAIL_HOST_USER

  try:
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    messages.success(request, "E-Mail an " + str(to) + " wurde versandt")
  except:
    messages.error(request, "E-Mail an " + str(to) + " konnte nicht versandt werden!")

  message_att = 'Anhänge zu ' + subject
  email = EmailMessage(subject, message_att, from_email, [to])
  files = context['file_list']
  path_pk = str(pk)

  try:
    for file in files:
      path = os.path.join(settings.MEDIA_ROOT, str('attachments/' + path_pk + '/' + file.file_name))
      email.attach_file(path, mimetype=None)

    email.send()
    messages.success(request, "Anhänge an " + str(to) + " wurden versandt")

  except:
    messages.error(request, "Anhänge an " + str(to) +
                   "konnten nicht versandt werden (nur <Dateiname>.pdf, .img oder .png erlaubt)")

  return render(request, 'expenses/travel_list.html', context)


def event_genPDF(request, pk):
  event = get_object_or_404(Event, pk=pk)
  rates = get_object_or_404(Rates, id=1)
  context = create_context_days(event, rates)
  pdf = render_to_pdf('expenses/travel_pdf.html', context)
  if pdf:
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = 'Reiseabrechnung.pdf'
    content = "inline; filename=%s" % filename
    response['Content-Disposition'] = content
    return response
  return render(request, 'expenses/travel_list.html', context)


class AboutView(TemplateView):
  template_name = 'expenses/about.html'

def travel_list(request, pk):
  event = get_object_or_404(Event, pk=pk)
  # user_id = request.user.id
  rates = get_object_or_404(Rates, id=1)

  context = create_context_days(event, rates)
  return render(request, 'expenses/travel_list.html', context)


def days_add(request, pk):
  form = DaysForm()
  event = get_object_or_404(Event, pk=pk)
  rates = Rates.objects.get(id=1)
  context = {
    'event': event,
    'form': form,
    'rates': rates,
  }

  if request.method == 'POST':
    form = DaysForm(request.POST)

    if form.is_valid():
      days = form.save(commit=False)
      days.event = event
      days = form.save(commit=True)
      days.save()

      context = create_context_days(event, rates)
      return render(request, 'expenses/travel_list.html', context)

  return render(request, 'expenses/days_form.html', context)


def days_update(request, pk):
  event = Event.objects.get(pk=pk)
  days_list = Days.objects.filter(event=event)
  days = days_list.first()
  rates = Rates.objects.get(id=1)

  if request.method == "POST":
    form = DaysForm(request.POST, instance=days)

    if form.is_valid():
      days = form.save(commit=False)
      days.event = event
      days = form.save(commit=True)
      days.save()

      context = create_context_days(event, rates)

      return render(request, 'expenses/travel_list.html', context)
      # return redirect('expenses:travel_list', pk=pk)
  else:
    context = create_context_days(event, rates)
    return render(request, 'expenses/days_form.html', context)


def create_context_days(event, rates):
  referee_id = event.referee_id
  referee = Referee.objects.get(author_id=referee_id)

  file_list = UploadedFile.objects.filter(event=event)

  travel_list = Travel.objects.filter(event=event)
  gefkm = 0
  for travel in travel_list:
    gefkm += travel.km

  kmallowence = Decimal(rates.kmallowence)
  dKG = gefkm * kmallowence
  kilometergeld = format(dKG, "3.2f")

  icount = 0
  if Days.objects.filter(event=event).exists():
    days_list = Days.objects.filter(event=event)
    days = days_list.first()
    icount = 1
    Tagegeld = format(days.iNOfOneDayTravel * Decimal(rates.dailyallowence), "3.2f")
    AnAbTagegeld = format(days.iNOfMoreDaysTravel * Decimal(rates.dailyallowence), "3.2f")
    ZwTagegeld = format(days.iNOfDaysBetween * Decimal(rates.fulldayallowence), "3.2f")
    Aufwand = format(days.iNOfTravelDays * Decimal(rates.dailycompensation), "3.2f")
    Breakfast = format(days.iNOfNights * Decimal(rates.bfreduction), "3.2f")
    CostAll = float(Tagegeld) + float(AnAbTagegeld) + float(ZwTagegeld) + float(Aufwand) + float(Breakfast)
    CostAll = format(CostAll, "3.2f")
    Erstattungsbetrag = float(CostAll) + float(dKG)
    Erstattungsbetrag = format(Erstattungsbetrag, "3.2f")

    form = DaysForm(instance=days)

    context_days = {
      'form': form,
      'rates': rates,
      'referee': referee,
      'event': event,
      'travel_list': travel_list,
      'file_list': file_list,
      'gefkm': gefkm,
      'Kilometergeld': kilometergeld,
      'icount': icount,
      'days_list': days_list,
      'Tagegeld': Tagegeld, 'AnAbTagegeld': AnAbTagegeld, 'ZwTagegeld': ZwTagegeld,
      'Aufwand': Aufwand, 'Breakfast': Breakfast, 'CostAll': CostAll,
      'Erstattungsbetrag': Erstattungsbetrag,
    }
  else:
    context_days = {
      'referee': referee,
      'event': event,
      'travel_list': travel_list,
      'file_list': file_list,
      'gefkm': gefkm,
      'Kilometergeld': kilometergeld,
      'icount': icount,
    }
  return context_days


def travel_add(request, pk):
  form = TravelForm()
  event = get_object_or_404(Event, pk=pk)
  context = {
    'event': event,
    'form': form
  }

  if request.method == 'POST':
    form = TravelForm(request.POST)
    # st_date = request.POST.get('startdate')

    if form.is_valid():
      st_date = form.cleaned_data['traveldate']
      st_time = form.cleaned_data['starttime']
      ed_time = form.cleaned_data['endtime']
      duration = calc_duration(st_date, st_time, ed_time)

      referee_id = Event.objects.get(pk=pk).referee_id
      referee = Referee.objects.get(author_id=referee_id)

      rates = Rates.objects.get(id=1)
      kmallowence = Decimal(rates.kmallowence)
      travel_list = Travel.objects.filter(event=event)
      gefkm = 0
      for travel in travel_list:
        gefkm += travel.km
      # dKG = gefkm * kmallowence
      # Kilometergeld = format(dKG, "3.2f")

      travel = form.save(commit=False)
      travel.event = event
      travel.duration = duration
      travel = form.save(commit=True)
      travel.save()

      # travel_list = Travel.objects.filter(event=event)
      context = {
        'event': event,
        'referee': referee,
        'travel_list': travel_list,
      }
    return render(request, 'expenses/travel_list.html', context)

  return render(request, 'expenses/travel_form.html', context)


def calc_duration(st_date, st_time, ed_time):
  st_date_str = st_date.strftime("%Y-%m-%d")

  st_time_str = st_time.strftime("%H:%M")
  st_time_full = st_date_str + " " + st_time_str
  st_time_dt = datetime.strptime(st_time_full, "%Y-%m-%d %H:%M")

  ed_time_str = ed_time.strftime("%H:%M")
  ed_time_full = st_date_str + " " + ed_time_str
  ed_time_dt = datetime.strptime(ed_time_full, "%Y-%m-%d %H:%M")

  duration = ed_time_dt - st_time_dt
  duration = duration.total_seconds()
  d_min = duration / 60
  d_h = str(d_min // 60)
  d_m = str(d_min % 60)
  d_h = d_h.partition('.')[0]
  d_m = d_m.partition('.')[0]
  duration_str = d_h + ":" + d_m

  return duration_str


def travel_update(request, pk, id):
  event = Event.objects.get(pk=pk)
  travel = Travel.objects.get(id=id)

  if request.method == "POST":
    form = TravelForm(request.POST, instance=travel)

    if form.is_valid():
      st_date = form.cleaned_data['traveldate']
      st_time = form.cleaned_data['starttime']
      ed_time = form.cleaned_data['endtime']
      duration = calc_duration(st_date, st_time, ed_time)

      referee_id = event.referee_id
      referee = Referee.objects.get(author_id=referee_id)

      travel = form.save(commit=False)
      travel.event = event
      travel.duration = duration
      travel = form.save(commit=True)
      travel.save()

      travel_list = Travel.objects.filter(event=event)

      context = {
        'pk': event.pk,
        'id': travel.id,
        'event': event,
        'referee': referee,
        'travel_list': travel_list,
      }
      return redirect('expenses:travel_list', pk=pk)
  else:
    travel = Travel.objects.get(id=id)
    form = TravelForm(instance=travel)
    context = {
      'event': event,
      'form': form
    }

    return render(request, 'expenses/travel_form.html', context)


def travel_delete(request, pk, id):
  event = get_object_or_404(Event, pk=pk)
  travel = Travel.objects.get(id=id)
  context = {
    'event': event,
    'travel': travel
  }
  if request.method == "GET":
    return render(request, 'expenses/travel_confirm_delete.html', context)
  elif request.method == 'POST':
    travel.delete()
    messages.success(request, "Fahrt wurde gelöscht")
    return redirect('expenses:travel_list', pk=pk)


class EventListView(LoginRequiredMixin, ListView):
  model = Event
  template_name = 'expenses/event_list.html'
  context_object_name = 'event'

  def get_queryset(self):
    qs = super().get_queryset()
    qs = qs.filter(referee_id=self.request.user.id)
    qs = qs.order_by("-startdate")
    return qs

  def get_context_data(self, **kwargs):
    user_id = self.request.user.id
    referee_list = Referee.objects.all().filter(author_id=user_id)
    referee = referee_list[0]  # nur eine Zeile/Object pro Referee
    referee_id = referee.author_id
    event_list = Event.objects.all().filter(referee_id=referee_id).order_by('-startdate')
    context = {
      'referee': referee,
      'event_list': event_list,
    }
    return context


class EventCreateView(LoginRequiredMixin, CreateView):
  model = Event
  form_class = EventForm
  template_name = 'expenses/event_form.html'
  success_url = reverse_lazy('expenses:event_list')

  def form_invalid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def form_valid(self, form):
    referee_id = self.request.user.id
    form.instance.referee_id = referee_id
    form.save()
    # event_new = form.save(commit=False)
    # event_new.save()
    # event_list = Event.objects.all().filter(referee_id=referee_id).order_by('startdate')
    return super().form_valid(form)


class EventDetailView(DetailView):
  template_name = "expenses/travel_list.html"
  model = Event

  def get_context_data(self, **kwargs):
    event = Event.objects.get(pk=self.kwargs['pk'])
    referee_id = event.referee_id
    referee_list = Referee.objects.filter(author_id=referee_id)
    referee = referee_list[0]
    context = {
      'event': event,
      'referee': referee,
      'event_id': event.id,
    }
    return context


class EventUpdateView(LoginRequiredMixin, UpdateView):
  model = Event
  form_class = EventForm
  template_name = "expenses/event_form.html"

  def get_success_url(self):
    return reverse('expenses:event_list')


class EventDeleteView(DeleteView):
  model = Event
  context_object_name = "event"
  success_url = reverse_lazy('expenses:event_list')
  success_message = "%(name)s gelöscht"
  def get_success_message(self, cleaned_data):
    return self.get_success_message(dict(
      cleaned_data,
      name=cleaned_data['name']
    ))

  def form_valid(self, form):
    messages.success(self.request, "Abrechnung gelöscht.")
    return super(EventDeleteView, self).form_valid(form)


def referee_settings(request):
  author = request.user
  referee_list = Referee.objects.filter(author=author)
  context = {}
  if referee_list.count() > 0:
    referee_instance = referee_list.first()
    context['referee'] = referee_instance
    return render(request, 'expenses/referee_detail.html', context)
  else:
    form = RefereeForm()
    context['form'] = form
    context['author'] = request.user
    return render(request, 'expenses/referee_form.html', context)


def referee_update(request, pk):
  referee = get_object_or_404(Referee, pk=pk)
  if request.method == 'POST':
    form = RefereeForm(request.POST, instance=referee)
    if form.is_valid():
      referee = form.save(commit=False)
      referee.author = request.user
      # referee.id = 1
      referee.save()
      event_list = Event.objects.all().filter(referee_id=referee.author_id).order_by('-startdate')
      context = {
        'referee': referee,
        'event_list': event_list,
      }
      return render(request, 'expenses/event_list.html', context)
      # return render(request, 'expenses/referee_detail.html', context)
    else:
      if 'IBAN' in form.errors:
        messages.error(request, 'IBAN nicht korrekt!')

  else:
    form = RefereeForm(instance=referee)
  return render(request, 'expenses/referee_form.html', {'form': form})
