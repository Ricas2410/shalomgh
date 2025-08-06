"""
Views for ministry and group management.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Ministry, MinistryGallery
from core.models import SiteSetting


class MinistryListView(ListView):
    """View for listing all ministries with filtering and search."""

    model = Ministry
    template_name = 'ministries/list.html'
    context_object_name = 'ministries'
    paginate_by = 12

    def get_queryset(self):
        """Get filtered and searched ministries."""
        queryset = Ministry.objects.filter(is_active=True).select_related('leader').prefetch_related('assistant_leaders')

        # Search functionality
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(activities__icontains=search_query)
            )

        # Filter by ministry type
        ministry_type = self.request.GET.get('type', '').strip()
        if ministry_type and ministry_type != 'all':
            queryset = queryset.filter(ministry_type=ministry_type)

        # Filter by age group
        age_filter = self.request.GET.get('age', '').strip()
        if age_filter:
            if age_filter == 'children':
                queryset = queryset.filter(
                    Q(ministry_type='children') |
                    Q(max_age__lte=12)
                )
            elif age_filter == 'youth':
                queryset = queryset.filter(
                    Q(ministry_type='youth') |
                    (Q(min_age__gte=13) & Q(max_age__lte=25))
                )
            elif age_filter == 'adults':
                queryset = queryset.filter(
                    Q(min_age__gte=18) |
                    Q(min_age__isnull=True, max_age__isnull=True)
                )

        # Order by featured first, then display order
        return queryset.order_by('-is_featured', 'display_order', 'name')

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)

        # Add site settings
        context['site_settings'] = SiteSetting.get_settings()

        # Add filter options
        context['ministry_types'] = Ministry.MINISTRY_TYPE_CHOICES
        context['current_search'] = self.request.GET.get('search', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_age'] = self.request.GET.get('age', '')

        # Add featured ministries
        context['featured_ministries'] = Ministry.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('leader')[:3]

        # Add ministry statistics
        context['total_ministries'] = Ministry.objects.filter(is_active=True).count()
        context['ministry_type_counts'] = dict(
            Ministry.objects.filter(is_active=True)
            .values_list('ministry_type')
            .annotate(count=Count('ministry_type'))
        )

        # Add age group filters
        context['age_filters'] = [
            ('all', 'All Ages'),
            ('children', 'Children (0-12)'),
            ('youth', 'Youth (13-25)'),
            ('adults', 'Adults (18+)'),
        ]

        return context


class MinistryDetailView(DetailView):
    """View for individual ministry details."""

    model = Ministry
    template_name = 'ministries/detail.html'
    context_object_name = 'ministry'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Get ministry with related data."""
        return Ministry.objects.filter(is_active=True).select_related(
            'leader'
        ).prefetch_related(
            'assistant_leaders',
            'gallery_images'
        )

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)

        # Add site settings
        context['site_settings'] = SiteSetting.get_settings()

        # Add gallery images
        context['gallery_images'] = self.object.gallery_images.all()[:12]

        # Add related ministries (same type, excluding current)
        context['related_ministries'] = Ministry.objects.filter(
            ministry_type=self.object.ministry_type,
            is_active=True
        ).exclude(id=self.object.id).select_related('leader')[:4]

        # Add other ministries if no related ministries found
        if not context['related_ministries']:
            context['other_ministries'] = Ministry.objects.filter(
                is_active=True
            ).exclude(id=self.object.id).select_related('leader')[:4]

        # Add leadership information
        context['all_leaders'] = []
        if self.object.leader:
            context['all_leaders'].append(self.object.leader)
        context['all_leaders'].extend(self.object.assistant_leaders.all())

        return context
