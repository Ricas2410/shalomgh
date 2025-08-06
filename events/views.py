"""
Views for the events app.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
import calendar
import json

from .models import Event, EventCategory
from core.models import SiteSetting


class EventListView(ListView):
    """List view for events with filtering and search."""

    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        queryset = Event.objects.filter(is_published=True).select_related('category')

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(location_name__icontains=search_query)
            )

        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Event type filter
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        # Date filter
        date_filter = self.request.GET.get('date')
        today = timezone.now().date()

        if date_filter == 'upcoming':
            queryset = queryset.filter(start_date__gte=today)
        elif date_filter == 'past':
            queryset = queryset.filter(start_date__lt=today)
        elif date_filter == 'this_week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            queryset = queryset.filter(start_date__range=[week_start, week_end])
        elif date_filter == 'this_month':
            queryset = queryset.filter(
                start_date__year=today.year,
                start_date__month=today.month
            )

        return queryset.order_by('start_date', 'start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add site settings
        context['site_settings'] = SiteSetting.get_settings()

        # Add featured events
        context['featured_events'] = Event.objects.filter(
            is_published=True,
            is_featured=True,
            start_date__gte=timezone.now().date()
        ).select_related('category')[:3]

        # Add categories for filtering
        context['categories'] = EventCategory.objects.filter(is_active=True)

        # Add event types for filtering
        context['event_types'] = Event.EVENT_TYPE_CHOICES

        # Add current filters
        context['current_search'] = self.request.GET.get('search', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_date'] = self.request.GET.get('date', '')

        # Add upcoming events count
        context['upcoming_count'] = Event.objects.filter(
            is_published=True,
            start_date__gte=timezone.now().date()
        ).count()

        return context


class EventDetailView(DetailView):
    """Detail view for individual events."""

    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        return Event.objects.filter(is_published=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add site settings
        context['site_settings'] = SiteSetting.get_settings()

        # Add related events (same category, excluding current event)
        if self.object.category:
            context['related_events'] = Event.objects.filter(
                category=self.object.category,
                is_published=True,
                start_date__gte=timezone.now().date()
            ).exclude(pk=self.object.pk).select_related('category')[:4]

        # Add other upcoming events
        context['other_events'] = Event.objects.filter(
            is_published=True,
            start_date__gte=timezone.now().date()
        ).exclude(pk=self.object.pk).select_related('category')[:6]

        return context


class EventCalendarView(TemplateView):
    """Calendar view for events."""

    template_name = 'events/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add site settings
        context['site_settings'] = SiteSetting.get_settings()

        # Get current month and year from URL parameters or use current
        today = timezone.now().date()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))

        # Ensure valid month/year
        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1

        context['current_year'] = year
        context['current_month'] = month
        context['current_month_name'] = calendar.month_name[month]

        # Calculate previous and next month
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        context['prev_month'] = prev_month
        context['prev_year'] = prev_year
        context['next_month'] = next_month
        context['next_year'] = next_year

        # Get events for the current month
        month_start = datetime(year, month, 1).date()
        if month == 12:
            month_end = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            month_end = datetime(year, month + 1, 1).date() - timedelta(days=1)

        events = Event.objects.filter(
            is_published=True,
            start_date__range=[month_start, month_end]
        ).select_related('category').order_by('start_date', 'start_time')

        context['events'] = events

        # Add categories for filtering
        context['categories'] = EventCategory.objects.filter(is_active=True)

        return context


class EventAPIView(TemplateView):
    """API view for calendar events (JSON response)."""

    def get(self, request, *args, **kwargs):
        # Get date range from request
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
        else:
            # Default to current month
            today = timezone.now().date()
            start_date = datetime(today.year, today.month, 1).date()
            if today.month == 12:
                end_date = datetime(today.year + 1, 1, 1).date() - timedelta(days=1)
            else:
                end_date = datetime(today.year, today.month + 1, 1).date() - timedelta(days=1)

        # Get events in date range
        events = Event.objects.filter(
            is_published=True,
            start_date__range=[start_date, end_date]
        ).select_related('category')

        # Format events for calendar
        event_list = []
        for event in events:
            event_data = {
                'id': event.pk,
                'title': event.title,
                'start': event.start_date.isoformat(),
                'url': event.get_absolute_url(),
                'description': event.short_description or event.description[:100],
                'location': event.location_name,
                'allDay': event.is_all_day,
                'backgroundColor': event.category.color if event.category else '#0EC6EB',
                'borderColor': event.category.color if event.category else '#0EC6EB',
                'textColor': '#ffffff',
                'classNames': [f'event-{event.event_type}']
            }

            # Add end date if different from start date
            if event.end_date and event.end_date != event.start_date:
                event_data['end'] = event.end_date.isoformat()

            # Add time if not all day
            if not event.is_all_day and event.start_time:
                event_data['start'] = f"{event.start_date.isoformat()}T{event.start_time.isoformat()}"
                if event.end_time:
                    end_datetime = event.end_date or event.start_date
                    event_data['end'] = f"{end_datetime.isoformat()}T{event.end_time.isoformat()}"

            event_list.append(event_data)

        return JsonResponse(event_list, safe=False)
