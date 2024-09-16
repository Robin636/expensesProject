from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from expenses import views

app_name = 'expenses'

urlpatterns = ([
  path('', views.index, name='index'),
  path('admin/', admin.site.urls),
  path('accounts/', include('django.contrib.auth.urls')),

  path('about/', views.AboutView.as_view(), name='about'),

  path('expenses/', views.EventListView.as_view(), name='event_list'),

  path('event/add/', views.EventCreateView.as_view(), name='event_add'),
  path('event/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
  path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
  path('event/<int:pk>/genPDF/', views.event_genPDF, name='event_genPDF'),
  path('event/<int:pk>/uploadAtt/', views.upload_file, name='upload_file'),
  path('event/<int:pk>/delAtt/<int:id>/', views.delete_file, name='delete_file'),
  path('event/<int:pk>/send/', views.event_send, name='event_send'),

  path('event/<int:pk>/travel/', views.travel_list, name='travel_list'),
  path('event/<int:pk>/travel/add/', views.travel_add, name='travel_add'),
  path('event/<int:pk>/travel/<int:id>/', views.travel_update, name='travel_update'),
  path('event/<int:pk>/travel/<int:id>/delete/', views.travel_delete, name='travel_delete'),

  path('event/<int:pk>/days/add/', views.days_add, name='days_add'),
  path('event/<int:pk>/days/', views.days_update, name='days_update'),

  path('referee/settings', views.referee_settings, name='referee_settings'),
  path('referee/<int:pk>/update/', views.referee_update, name='referee_update'),

])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               
# if settings.DEBUG:
#   assert isinstance(settings.MEDIA_ROOT, object)
#   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
