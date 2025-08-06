"""
Events app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('calendar/', views.EventCalendarView.as_view(), name='calendar'),
    path('api/events/', views.EventAPIView.as_view(), name='api_events'),
]
