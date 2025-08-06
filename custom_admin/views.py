from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

# Import models from different apps
from core.models import SiteSetting, ContactMessage, ServiceTime
from sermons.models import Sermon, Speaker, SermonSeries
from events.models import Event, EventCategory
from ministries.models import Ministry, MinistryGallery
from pages.models import LeadershipProfile


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only staff users can access admin views."""

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('custom_admin:login')
        messages.error(self.request, 'You do not have permission to access this area.')
        return redirect('custom_admin:login')


class AdminLoginView(TemplateView):
    """Custom admin login view."""
    template_name = 'custom_admin/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('custom_admin:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                next_url = request.GET.get('next', 'custom_admin:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions.')
        else:
            messages.error(request, 'Please provide both username and password.')

        return self.get(request)


class AdminLogoutView(TemplateView):
    """Custom admin logout view."""

    def get(self, request):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('custom_admin:login')


class DashboardView(AdminRequiredMixin, TemplateView):
    """Main admin dashboard view."""
    template_name = 'custom_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get dashboard statistics
        context.update({
            'total_sermons': Sermon.objects.count(),
            'published_sermons': Sermon.objects.filter(is_published=True).count(),
            'total_events': Event.objects.count(),
            'upcoming_events': Event.objects.filter(start_date__gte=timezone.now().date()).count(),
            'total_ministries': Ministry.objects.count(),
            'active_ministries': Ministry.objects.filter(is_active=True).count(),
            'total_leaders': LeadershipProfile.objects.count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'recent_sermons': Sermon.objects.select_related('speaker', 'series').order_by('-created_at')[:5],
            'upcoming_events_list': Event.objects.filter(start_date__gte=timezone.now().date()).order_by('start_date')[:5],
            'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
        })

        return context


# Sermon Management Views
class SermonListView(AdminRequiredMixin, ListView):
    """List all sermons with search and filter capabilities."""
    model = Sermon
    template_name = 'custom_admin/sermon_list.html'
    context_object_name = 'sermons'
    paginate_by = 20

    def get_queryset(self):
        queryset = Sermon.objects.select_related('speaker', 'series').order_by('-date_preached')

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(speaker__name__icontains=search) |
                Q(series__title__icontains=search)
            )

        # Filter by published status
        status = self.request.GET.get('status')
        if status == 'published':
            queryset = queryset.filter(is_published=True)
        elif status == 'draft':
            queryset = queryset.filter(is_published=False)

        # Filter by speaker
        speaker_id = self.request.GET.get('speaker')
        if speaker_id:
            queryset = queryset.filter(speaker_id=speaker_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['speakers'] = Speaker.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['speaker'] = self.request.GET.get('speaker', '')
        return context


class SermonCreateView(AdminRequiredMixin, CreateView):
    """Create a new sermon."""
    model = Sermon
    template_name = 'custom_admin/sermon_form.html'
    fields = [
        'title', 'description', 'speaker', 'series', 'date_preached',
        'duration', 'media_type', 'video_url', 'audio_file', 'notes',
        'transcript', 'scripture_references', 'tags', 'thumbnail', 'pdf_notes',
        'is_published', 'is_featured', 'meta_description'
    ]
    success_url = reverse_lazy('custom_admin:sermon_list')

    def form_valid(self, form):
        messages.success(self.request, f'Sermon "{form.instance.title}" created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below. Check that all uploaded files are valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Sermon'
        context['speakers'] = Speaker.objects.all()
        context['series'] = SermonSeries.objects.all()
        return context


class SermonUpdateView(AdminRequiredMixin, UpdateView):
    """Update an existing sermon."""
    model = Sermon
    template_name = 'custom_admin/sermon_form.html'
    fields = [
        'title', 'description', 'speaker', 'series', 'date_preached',
        'duration', 'media_type', 'video_url', 'audio_file', 'notes',
        'transcript', 'scripture_references', 'tags', 'thumbnail', 'pdf_notes',
        'is_published', 'is_featured', 'meta_description'
    ]
    success_url = reverse_lazy('custom_admin:sermon_list')

    def form_valid(self, form):
        messages.success(self.request, f'Sermon "{form.instance.title}" updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below. Check that all uploaded files are valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Sermon: {self.object.title}'
        context['speakers'] = Speaker.objects.all()
        context['series'] = SermonSeries.objects.all()
        return context


class SermonDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a sermon."""
    model = Sermon
    template_name = 'custom_admin/confirm_delete.html'
    success_url = reverse_lazy('custom_admin:sermon_list')

    def delete(self, request, *args, **kwargs):
        sermon = self.get_object()
        messages.success(request, f'Sermon "{sermon.title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Sermon'
        context['cancel_url'] = reverse('custom_admin:sermon_list')
        return context


# Event Management Views
class EventListView(AdminRequiredMixin, ListView):
    """List all events with search and filter capabilities."""
    model = Event
    template_name = 'custom_admin/event_list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        queryset = Event.objects.select_related('category').order_by('-start_date')

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )

        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by event type
        event_type = self.request.GET.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        # Filter by date range
        date_filter = self.request.GET.get('date_filter')
        today = timezone.now().date()
        if date_filter == 'upcoming':
            queryset = queryset.filter(start_date__gte=today)
        elif date_filter == 'past':
            queryset = queryset.filter(start_date__lt=today)
        elif date_filter == 'this_month':
            start_of_month = today.replace(day=1)
            if today.month == 12:
                end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            queryset = queryset.filter(start_date__range=[start_of_month, end_of_month])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        context['event_types'] = Event.EVENT_TYPE_CHOICES
        context['search'] = self.request.GET.get('search', '')
        context['category'] = self.request.GET.get('category', '')
        context['event_type'] = self.request.GET.get('event_type', '')
        context['date_filter'] = self.request.GET.get('date_filter', '')
        return context


class EventCreateView(AdminRequiredMixin, CreateView):
    """Create a new event."""
    model = Event
    template_name = 'custom_admin/event_form.html'
    fields = [
        'title', 'description', 'short_description', 'category', 'event_type',
        'start_date', 'end_date', 'start_time', 'end_time', 'is_all_day',
        'location_name', 'address', 'registration_url', 'requires_registration',
        'max_attendees', 'contact_email', 'contact_phone', 'featured_image',
        'recurrence', 'recurrence_end_date', 'is_published', 'is_featured'
    ]
    success_url = reverse_lazy('custom_admin:event_list')

    def form_valid(self, form):
        messages.success(self.request, f'Event "{form.instance.title}" created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below. Check that all uploaded files are valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Event'
        context['categories'] = EventCategory.objects.all()
        return context


class EventUpdateView(AdminRequiredMixin, UpdateView):
    """Update an existing event."""
    model = Event
    template_name = 'custom_admin/event_form.html'
    fields = [
        'title', 'description', 'short_description', 'category', 'event_type',
        'start_date', 'end_date', 'start_time', 'end_time', 'is_all_day',
        'location_name', 'address', 'registration_url', 'requires_registration',
        'max_attendees', 'contact_email', 'contact_phone', 'featured_image',
        'recurrence', 'recurrence_end_date', 'is_published', 'is_featured'
    ]
    success_url = reverse_lazy('custom_admin:event_list')

    def form_valid(self, form):
        messages.success(self.request, f'Event "{form.instance.title}" updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below. Check that all uploaded files are valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Event: {self.object.title}'
        context['categories'] = EventCategory.objects.all()
        return context


class EventDeleteView(AdminRequiredMixin, DeleteView):
    """Delete an event."""
    model = Event
    template_name = 'custom_admin/confirm_delete.html'
    success_url = reverse_lazy('custom_admin:event_list')

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        messages.success(request, f'Event "{event.title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Event'
        context['cancel_url'] = reverse('custom_admin:event_list')
        return context


# Ministry Management Views
class MinistryListView(AdminRequiredMixin, ListView):
    """List all ministries with search and filter capabilities."""
    model = Ministry
    template_name = 'custom_admin/ministry_list.html'
    context_object_name = 'ministries'
    paginate_by = 20

    def get_queryset(self):
        queryset = Ministry.objects.select_related('leader').order_by('name')

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(leader__name__icontains=search)
            )

        # Filter by ministry type
        ministry_type = self.request.GET.get('ministry_type')
        if ministry_type:
            queryset = queryset.filter(ministry_type=ministry_type)

        # Filter by active status
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ministry_types'] = Ministry.MINISTRY_TYPE_CHOICES
        context['search'] = self.request.GET.get('search', '')
        context['ministry_type'] = self.request.GET.get('ministry_type', '')
        context['status'] = self.request.GET.get('status', '')
        return context


class MinistryCreateView(AdminRequiredMixin, CreateView):
    """Create a new ministry."""
    model = Ministry
    template_name = 'custom_admin/ministry_form.html'
    fields = [
        'name', 'ministry_type', 'short_description', 'description',
        'mission_statement', 'leader', 'assistant_leaders', 'contact_email',
        'contact_phone', 'meeting_day', 'meeting_time', 'meeting_location',
        'min_age', 'max_age', 'featured_image', 'activities', 'requirements',
        'is_active', 'is_featured', 'display_order'
    ]
    success_url = reverse_lazy('custom_admin:ministry_list')

    def form_valid(self, form):
        messages.success(self.request, f'Ministry "{form.instance.name}" created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below. Check that all uploaded files are valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Ministry'
        context['leaders'] = LeadershipProfile.objects.all()
        return context


class MinistryUpdateView(AdminRequiredMixin, UpdateView):
    """Update an existing ministry."""
    model = Ministry
    template_name = 'custom_admin/ministry_form.html'
    fields = [
        'name', 'ministry_type', 'short_description', 'description',
        'mission_statement', 'leader', 'assistant_leaders', 'contact_email',
        'contact_phone', 'meeting_day', 'meeting_time', 'meeting_location',
        'min_age', 'max_age', 'featured_image', 'activities', 'requirements',
        'is_active', 'is_featured', 'display_order'
    ]
    success_url = reverse_lazy('custom_admin:ministry_list')

    def form_valid(self, form):
        messages.success(self.request, f'Ministry "{form.instance.name}" updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below. Check that all uploaded files are valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Ministry: {self.object.name}'
        context['leaders'] = LeadershipProfile.objects.all()
        return context


class MinistryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a ministry."""
    model = Ministry
    template_name = 'custom_admin/confirm_delete.html'
    success_url = reverse_lazy('custom_admin:ministry_list')

    def delete(self, request, *args, **kwargs):
        ministry = self.get_object()
        messages.success(request, f'Ministry "{ministry.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Ministry'
        context['cancel_url'] = reverse('custom_admin:ministry_list')
        return context


# Ministry Gallery Management Views
class MinistryGalleryView(AdminRequiredMixin, ListView):
    """List gallery images for a specific ministry."""
    model = MinistryGallery
    template_name = 'custom_admin/ministry_gallery.html'
    context_object_name = 'gallery_images'
    paginate_by = 20

    def get_queryset(self):
        self.ministry = get_object_or_404(Ministry, pk=self.kwargs['ministry_id'])
        return MinistryGallery.objects.filter(ministry=self.ministry).order_by('display_order', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ministry'] = self.ministry
        context['title'] = f'Gallery: {self.ministry.name}'
        return context


class MinistryGalleryCreateView(AdminRequiredMixin, CreateView):
    """Add a new gallery image to a ministry."""
    model = MinistryGallery
    template_name = 'custom_admin/ministry_gallery_form.html'
    fields = ['image', 'caption', 'display_order']

    def form_valid(self, form):
        self.ministry = get_object_or_404(Ministry, pk=self.kwargs['ministry_id'])
        form.instance.ministry = self.ministry
        messages.success(self.request, 'Gallery image added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('custom_admin:ministry_gallery', kwargs={'ministry_id': self.kwargs['ministry_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.ministry = get_object_or_404(Ministry, pk=self.kwargs['ministry_id'])
        context['ministry'] = self.ministry
        context['title'] = f'Add Gallery Image: {self.ministry.name}'
        return context


class MinistryGalleryUpdateView(AdminRequiredMixin, UpdateView):
    """Edit a gallery image."""
    model = MinistryGallery
    template_name = 'custom_admin/ministry_gallery_form.html'
    fields = ['image', 'caption', 'display_order']

    def form_valid(self, form):
        messages.success(self.request, 'Gallery image updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('custom_admin:ministry_gallery', kwargs={'ministry_id': self.object.ministry.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ministry'] = self.object.ministry
        context['title'] = f'Edit Gallery Image: {self.object.ministry.name}'
        return context


class MinistryGalleryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a gallery image."""
    model = MinistryGallery
    template_name = 'custom_admin/confirm_delete.html'

    def get_success_url(self):
        return reverse('custom_admin:ministry_gallery', kwargs={'ministry_id': self.object.ministry.pk})

    def delete(self, request, *args, **kwargs):
        gallery_image = self.get_object()
        messages.success(request, 'Gallery image deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Gallery Image'
        context['cancel_url'] = reverse('custom_admin:ministry_gallery', kwargs={'ministry_id': self.object.ministry.pk})
        return context


# Leadership Management Views
class LeadershipListView(AdminRequiredMixin, ListView):
    """List all leadership profiles."""
    model = LeadershipProfile
    template_name = 'custom_admin/leadership_list.html'
    context_object_name = 'leaders'
    paginate_by = 20

    def get_queryset(self):
        queryset = LeadershipProfile.objects.order_by('display_order', 'last_name', 'first_name')

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(position__icontains=search) |
                Q(bio__icontains=search)
            )

        # Filter by position
        position = self.request.GET.get('position')
        if position:
            queryset = queryset.filter(position=position)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position_choices'] = LeadershipProfile.POSITION_CHOICES
        context['search'] = self.request.GET.get('search', '')
        context['position'] = self.request.GET.get('position', '')
        return context


class LeadershipCreateView(AdminRequiredMixin, CreateView):
    """Create a new leadership profile."""
    model = LeadershipProfile
    template_name = 'custom_admin/leadership_form.html'
    fields = [
        'first_name', 'last_name', 'position', 'custom_position', 'bio', 'email', 'phone',
        'photo', 'years_in_ministry', 'specializations', 'display_order', 'is_active'
    ]
    success_url = reverse_lazy('custom_admin:leadership_list')

    def form_valid(self, form):
        messages.success(self.request, f'Leadership profile for "{form.instance.get_full_name()}" created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below. Check that all uploaded files are valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Leader'
        return context


class LeadershipUpdateView(AdminRequiredMixin, UpdateView):
    """Update an existing leadership profile."""
    model = LeadershipProfile
    template_name = 'custom_admin/leadership_form.html'
    fields = [
        'first_name', 'last_name', 'position', 'custom_position', 'bio', 'email', 'phone',
        'photo', 'years_in_ministry', 'specializations', 'display_order', 'is_active'
    ]
    success_url = reverse_lazy('custom_admin:leadership_list')

    def form_valid(self, form):
        messages.success(self.request, f'Leadership profile for "{form.instance.get_full_name()}" updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below. Check that all uploaded files are valid.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Leader: {self.object.get_full_name()}'
        return context


class LeadershipDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a leadership profile."""
    model = LeadershipProfile
    template_name = 'custom_admin/confirm_delete.html'
    success_url = reverse_lazy('custom_admin:leadership_list')

    def delete(self, request, *args, **kwargs):
        leader = self.get_object()
        messages.success(request, f'Leadership profile for "{leader.get_full_name()}" deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Leadership Profile'
        context['cancel_url'] = reverse('custom_admin:leadership_list')
        return context


# Site Settings View
class SiteSettingsView(AdminRequiredMixin, UpdateView):
    """Manage site settings."""
    model = SiteSetting
    template_name = 'custom_admin/site_settings.html'
    fields = [
        'site_name', 'church_name', 'tagline', 'welcome_message',
        'hero_title', 'hero_subtitle',
        'phone', 'email', 'address',
        'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url',
        'giving_platform_url', 'member_portal_url', 'google_maps_api_key',
        'enable_paystack', 'paystack_public_key', 'paystack_secret_key',
        'cta_image', 'cta_youtube_url'
    ]
    success_url = reverse_lazy('custom_admin:settings')

    def get_object(self):
        """Get or create the site settings object."""
        obj, created = SiteSetting.objects.get_or_create(pk=1)
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Site settings updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Site Settings'
        context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
        context['recent_messages'] = ContactMessage.objects.order_by('-created_at')[:10]
        return context


# Service Times Management Views
class ServiceTimeListView(AdminRequiredMixin, ListView):
    """List all service times."""
    model = ServiceTime
    template_name = 'custom_admin/service_time_list.html'
    context_object_name = 'service_times'
    ordering = ['display_order', 'day']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Service Times'
        return context


class ServiceTimeCreateView(AdminRequiredMixin, CreateView):
    """Create a new service time."""
    model = ServiceTime
    template_name = 'custom_admin/service_time_form.html'
    fields = ['name', 'day', 'time', 'display_order', 'is_active']
    success_url = reverse_lazy('custom_admin:service_time_list')

    def form_valid(self, form):
        messages.success(self.request, f'Service time "{form.instance.name}" created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Service Time'
        return context


class ServiceTimeUpdateView(AdminRequiredMixin, UpdateView):
    """Update an existing service time."""
    model = ServiceTime
    template_name = 'custom_admin/service_time_form.html'
    fields = ['name', 'day', 'time', 'display_order', 'is_active']
    success_url = reverse_lazy('custom_admin:service_time_list')

    def form_valid(self, form):
        messages.success(self.request, f'Service time "{form.instance.name}" updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Service Time: {self.object.name}'
        return context


class ServiceTimeDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a service time."""
    model = ServiceTime
    template_name = 'custom_admin/confirm_delete.html'
    success_url = reverse_lazy('custom_admin:service_time_list')

    def delete(self, request, *args, **kwargs):
        service_time = self.get_object()
        messages.success(request, f'Service time "{service_time.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Service Time'
        context['cancel_url'] = reverse('custom_admin:service_time_list')
        return context
