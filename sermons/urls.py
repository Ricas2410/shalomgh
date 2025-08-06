"""
Sermons app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'sermons'

urlpatterns = [
    path('', views.SermonListView.as_view(), name='list'),
    path('<int:pk>/', views.SermonDetailView.as_view(), name='detail'),
    path('series/', views.SermonSeriesListView.as_view(), name='series_list'),
    path('series/<slug:slug>/', views.SermonSeriesDetailView.as_view(), name='series_detail'),
    path('speakers/', views.SpeakerListView.as_view(), name='speakers'),
    path('speakers/<slug:slug>/', views.SpeakerDetailView.as_view(), name='speaker_detail'),
]
