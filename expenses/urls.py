from django.urls import include, path

from django.contrib import admin
from expenses import views

app_name = 'expenses'

urlpatterns = [
  path('', views.index, name='index'),
  path('admin/', admin.site.urls),
  path('accounts/', include('django.contrib.auth.urls')),

  path('about/', views.AboutView.as_view(), name='about'),
  # path('about/', views.about, name='about'),

  path('expenses/', views.EventListView.as_view(), name='event_list'),
  path('dailytravel/new/', views.DailytravelListView.as_view(), name='dt_new'),
  # path('<int:pk>/', views.ChapDetailView.as_view(), name='chap_detail'),
  # path('chap/<int:pk>/update/', views.ChapUpdateView.as_view(), name='chap_update'),
  # path('chap/<int:pk>/remove/', views.ChapDeleteView.as_view(), name='chap_remove'),
  #
  # path('chap/<int:pk>/add_pair_to_chap/', views.add_pair_to_chap, name='add_pair_to_chap'),
  # path('chap/<int:pk>/pair/<int:id>/edit/', views.pair_update, name='pair_edit'),
  # path('chap/<int:pk>/pair/<int:id>/remove/', views.pair_remove, name='pair_remove'),
  #
  # path('chap/<int:pk>/settings/', views.settings, name='settings'),
  # path('chap/<int:pk>/callReset/', views.callReset, name='callReset'),
  #
  # path('chap/<int:pk>/<int:ct>/callPairs/', views.callPairs, name='callPairs'),
  # path('chap/<int:pk>/<int:ct>/callPairs/next/', views.call_next, name='call_next'),
  #
  # path('chap/<int:pk>/pair/<int:id>/<int:ct>/<str:lr>/fail/', views.call_fail, name='call_fail'),
  # path('chap/<int:pk>/pair/<int:id>/<int:ct>/<str:lr>/OK/', views.call_OK, name='call_OK'),
]
