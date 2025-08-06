"""
URL configuration for livestream app.
"""
from django.urls import path
from . import views

app_name = 'livestream'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.LiveStreamDashboardView.as_view(), name='dashboard'),
    
    # Live Streams
    path('', views.LiveStreamListView.as_view(), name='list'),
    path('add/', views.LiveStreamCreateView.as_view(), name='add'),
    path('<int:pk>/', views.LiveStreamDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.LiveStreamUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.LiveStreamDeleteView.as_view(), name='delete'),
    
    # Platforms
    path('platforms/', views.StreamPlatformListView.as_view(), name='platform_list'),
    path('platforms/add/', views.StreamPlatformCreateView.as_view(), name='platform_add'),
    path('platforms/<int:pk>/edit/', views.StreamPlatformUpdateView.as_view(), name='platform_edit'),
    path('platforms/<int:pk>/delete/', views.StreamPlatformDeleteView.as_view(), name='platform_delete'),
    
    # API endpoints
    path('api/stream/<int:stream_id>/status/', views.stream_status_api, name='stream_status_api'),
    path('api/stream/<int:stream_id>/update-status/', views.update_stream_status, name='update_stream_status'),
]
