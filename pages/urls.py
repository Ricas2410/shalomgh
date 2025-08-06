"""
Pages app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.AboutView.as_view(), name='about'),
    path('our-story/', views.OurStoryView.as_view(), name='our_story'),
    path('beliefs/', views.BeliefsView.as_view(), name='beliefs'),
    path('leadership/', views.LeadershipView.as_view(), name='leadership'),
    path('leadership/<int:pk>/', views.LeadershipDetailView.as_view(), name='leadership_detail'),
    path('location/', views.LocationView.as_view(), name='location'),
    path('online-tv/', views.OnlineTVView.as_view(), name='online_tv'),
]
