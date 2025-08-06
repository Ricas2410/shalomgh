"""
Views for the sermons app.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Sermon, SermonSeries, Speaker
from core.models import SiteSetting


class SermonListView(ListView):
    """List view for sermons with filtering and search."""
    model = Sermon
    template_name = 'sermons/list.html'
    context_object_name = 'sermons'
    paginate_by = 12

    def get_queryset(self):
        queryset = Sermon.objects.filter(is_published=True).select_related(
            'speaker', 'series'
        ).prefetch_related('speaker__leadership_profile')

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(speaker__name__icontains=search_query) |
                Q(series__title__icontains=search_query) |
                Q(tags__icontains=search_query) |
                Q(scripture_references__icontains=search_query)
            )

        # Filter by speaker
        speaker_slug = self.request.GET.get('speaker')
        if speaker_slug:
            queryset = queryset.filter(speaker__slug=speaker_slug)

        # Filter by series
        series_slug = self.request.GET.get('series')
        if series_slug:
            queryset = queryset.filter(series__slug=series_slug)

        # Filter by date range
        date_filter = self.request.GET.get('date')
        if date_filter:
            today = timezone.now().date()
            if date_filter == 'this_month':
                start_date = today.replace(day=1)
                queryset = queryset.filter(date_preached__gte=start_date)
            elif date_filter == 'last_month':
                first_day_this_month = today.replace(day=1)
                last_month = first_day_this_month - timedelta(days=1)
                start_date = last_month.replace(day=1)
                queryset = queryset.filter(
                    date_preached__gte=start_date,
                    date_preached__lt=first_day_this_month
                )
            elif date_filter == 'this_year':
                start_date = today.replace(month=1, day=1)
                queryset = queryset.filter(date_preached__gte=start_date)
            elif date_filter == 'last_year':
                last_year = today.year - 1
                queryset = queryset.filter(date_preached__year=last_year)

        # Filter by media type
        media_type = self.request.GET.get('media_type')
        if media_type:
            queryset = queryset.filter(media_type=media_type)

        return queryset.order_by('-date_preached', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get filter options
        speakers = Speaker.objects.filter(
            is_active=True,
            sermons__is_published=True
        ).distinct().order_by('name')

        series = SermonSeries.objects.filter(
            is_active=True,
            sermons__is_published=True
        ).distinct().order_by('-start_date')

        # Get featured sermons
        featured_sermons = Sermon.objects.filter(
            is_published=True,
            is_featured=True
        ).select_related('speaker', 'series')[:3]

        # Get current filters
        current_filters = {
            'search': self.request.GET.get('search', ''),
            'speaker': self.request.GET.get('speaker', ''),
            'series': self.request.GET.get('series', ''),
            'date': self.request.GET.get('date', ''),
            'media_type': self.request.GET.get('media_type', ''),
        }

        context.update({
            'site_settings': site_settings,
            'speakers': speakers,
            'series': series,
            'featured_sermons': featured_sermons,
            'current_filters': current_filters,
            'media_type_choices': Sermon.MEDIA_TYPE_CHOICES,
        })

        return context


class SermonDetailView(DetailView):
    """Detail view for individual sermons."""
    model = Sermon
    template_name = 'sermons/detail.html'
    context_object_name = 'sermon'

    def get_queryset(self):
        return Sermon.objects.filter(is_published=True).select_related(
            'speaker', 'series'
        ).prefetch_related('speaker__leadership_profile')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.increment_view_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get related sermons (same series or speaker)
        related_sermons = Sermon.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk).select_related('speaker', 'series')

        if self.object.series:
            related_sermons = related_sermons.filter(
                series=self.object.series
            ).order_by('-date_preached')[:4]
        else:
            related_sermons = related_sermons.filter(
                speaker=self.object.speaker
            ).order_by('-date_preached')[:4]

        # Get sermon tags as list
        tags = self.object.get_tags_list()

        context.update({
            'site_settings': site_settings,
            'related_sermons': related_sermons,
            'tags': tags,
        })

        return context


class SermonSeriesListView(ListView):
    """List view for sermon series."""
    model = SermonSeries
    template_name = 'sermons/series_list.html'
    context_object_name = 'series_list'
    paginate_by = 12

    def get_queryset(self):
        queryset = SermonSeries.objects.filter(
            is_active=True,
            sermons__is_published=True
        ).annotate(
            sermon_count=Count('sermons', filter=Q(sermons__is_published=True))
        ).distinct().order_by('-start_date', 'title')

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get featured series
        featured_series = SermonSeries.objects.filter(
            is_active=True,
            is_featured=True,
            sermons__is_published=True
        ).annotate(
            sermon_count=Count('sermons', filter=Q(sermons__is_published=True))
        ).distinct()[:3]

        context.update({
            'site_settings': site_settings,
            'featured_series': featured_series,
            'search_query': self.request.GET.get('search', ''),
        })

        return context


class SermonSeriesDetailView(DetailView):
    """Detail view for sermon series."""
    model = SermonSeries
    template_name = 'sermons/series_detail.html'
    context_object_name = 'series'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return SermonSeries.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get sermons in this series
        sermons = Sermon.objects.filter(
            series=self.object,
            is_published=True
        ).select_related('speaker').order_by('-date_preached')

        # Get other series
        other_series = SermonSeries.objects.filter(
            is_active=True,
            sermons__is_published=True
        ).exclude(pk=self.object.pk).annotate(
            sermon_count=Count('sermons', filter=Q(sermons__is_published=True))
        ).distinct().order_by('-start_date')[:4]

        context.update({
            'site_settings': site_settings,
            'sermons': sermons,
            'other_series': other_series,
        })

        return context


class SpeakerListView(ListView):
    """List view for speakers."""
    model = Speaker
    template_name = 'sermons/speakers.html'
    context_object_name = 'speakers'
    paginate_by = 12

    def get_queryset(self):
        queryset = Speaker.objects.filter(
            is_active=True,
            sermons__is_published=True
        ).annotate(
            sermon_count=Count('sermons', filter=Q(sermons__is_published=True))
        ).distinct().order_by('name')

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(bio__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        context.update({
            'site_settings': site_settings,
            'search_query': self.request.GET.get('search', ''),
        })

        return context


class SpeakerDetailView(DetailView):
    """Detail view for speakers."""
    model = Speaker
    template_name = 'sermons/speaker_detail.html'
    context_object_name = 'speaker'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Speaker.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get sermons by this speaker
        sermons = Sermon.objects.filter(
            speaker=self.object,
            is_published=True
        ).select_related('series').order_by('-date_preached')

        # Get other speakers
        other_speakers = Speaker.objects.filter(
            is_active=True,
            sermons__is_published=True
        ).exclude(pk=self.object.pk).annotate(
            sermon_count=Count('sermons', filter=Q(sermons__is_published=True))
        ).distinct().order_by('name')[:4]

        context.update({
            'site_settings': site_settings,
            'sermons': sermons,
            'other_speakers': other_speakers,
        })

        return context
