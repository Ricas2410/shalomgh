"""
Ministries app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'ministries'

urlpatterns = [
    path('', views.MinistryListView.as_view(), name='list'),
    path('<slug:slug>/', views.MinistryDetailView.as_view(), name='detail'),
]
