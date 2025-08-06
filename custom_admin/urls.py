"""
Custom admin app URL configuration.
"""
from django.urls import path, include
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.AdminLoginView.as_view(), name='login'),
    path('logout/', views.AdminLogoutView.as_view(), name='logout'),
    
    # Sermon management
    path('sermons/', views.SermonListView.as_view(), name='sermon_list'),
    path('sermons/add/', views.SermonCreateView.as_view(), name='sermon_add'),
    path('sermons/<int:pk>/edit/', views.SermonUpdateView.as_view(), name='sermon_edit'),
    path('sermons/<int:pk>/delete/', views.SermonDeleteView.as_view(), name='sermon_delete'),
    
    # Event management
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/add/', views.EventCreateView.as_view(), name='event_add'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    # Ministry management
    path('ministries/', views.MinistryListView.as_view(), name='ministry_list'),
    path('ministries/add/', views.MinistryCreateView.as_view(), name='ministry_add'),
    path('ministries/<int:pk>/edit/', views.MinistryUpdateView.as_view(), name='ministry_edit'),
    path('ministries/<int:pk>/delete/', views.MinistryDeleteView.as_view(), name='ministry_delete'),
    path('ministries/<int:ministry_id>/gallery/', views.MinistryGalleryView.as_view(), name='ministry_gallery'),
    path('ministries/<int:ministry_id>/gallery/add/', views.MinistryGalleryCreateView.as_view(), name='ministry_gallery_add'),
    path('gallery/<int:pk>/edit/', views.MinistryGalleryUpdateView.as_view(), name='ministry_gallery_edit'),
    path('gallery/<int:pk>/delete/', views.MinistryGalleryDeleteView.as_view(), name='ministry_gallery_delete'),
    
    # Leadership management
    path('leadership/', views.LeadershipListView.as_view(), name='leadership_list'),
    path('leadership/add/', views.LeadershipCreateView.as_view(), name='leadership_add'),
    path('leadership/<int:pk>/edit/', views.LeadershipUpdateView.as_view(), name='leadership_edit'),
    path('leadership/<int:pk>/delete/', views.LeadershipDeleteView.as_view(), name='leadership_delete'),
    
    # Site settings
    path('settings/', views.SiteSettingsView.as_view(), name='settings'),
    path('service-times/', views.ServiceTimeListView.as_view(), name='service_time_list'),
    path('service-times/add/', views.ServiceTimeCreateView.as_view(), name='service_time_add'),
    path('service-times/<int:pk>/edit/', views.ServiceTimeUpdateView.as_view(), name='service_time_edit'),
    path('service-times/<int:pk>/delete/', views.ServiceTimeDeleteView.as_view(), name='service_time_delete'),
    
    # Live streaming
    path('livestream/', include('livestream.urls')),
]
