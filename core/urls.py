"""
Core app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('giving/', views.GivingView.as_view(), name='giving'),
    path('plan-visit/', views.PlanVisitView.as_view(), name='plan_visit'),
]
