from django.urls import include, path

from django.contrib import admin
from expenses import views

app_name = 'expenses'

urlpatterns = [
  path('', views.index, name='index'),
  path('admin/', admin.site.urls),
  path('accounts/', include('django.contrib.auth.urls')),

  path('about/', views.AboutView.as_view(), name='about'),

  path('expenses/', views.EventListView.as_view(), name='event_list'),

  path('event/add/', views.EventCreateView.as_view(), name='event_add'),
  path('event/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
  path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

  # path('event/new/', views.EventCreateView.as_view(), name='event_new'),
  # path('event/<int:pk>/',views.EventDetailView.as_view(), name='event_detail'),
  #
  # path('event/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
  # path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),



  path('referee/settings', views.referee_settings, name='referee_settings'),
  path('referee/<int:pk>/update/', views.referee_update, name='referee_update'),


]
