"""
Sitemap configuration for SEO.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home',
            'core:contact',
            'core:giving',
            'core:plan_visit',
            'pages:about',
            'pages:our_story',
            'pages:beliefs',
            'pages:leadership',
            'pages:location',
            'sermons:list',
            'sermons:series_list',
            'sermons:speakers',
            'events:list',
            'events:calendar',
            'ministries:list',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        """Return last modification date."""
        if item == 'core:home':
            return timezone.now() - timedelta(days=1)  # Home page changes frequently
        return timezone.now() - timedelta(days=7)  # Other pages change weekly


class SermonSitemap(Sitemap):
    """Sitemap for sermon pages."""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        from sermons.models import Sermon
        return Sermon.objects.filter(is_published=True).order_by('-date_preached')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class SermonSeriesSitemap(Sitemap):
    """Sitemap for sermon series pages."""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        from sermons.models import SermonSeries
        return SermonSeries.objects.filter(is_active=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class EventSitemap(Sitemap):
    """Sitemap for event pages."""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        from events.models import Event
        # Include upcoming events and recent past events
        cutoff_date = timezone.now() - timedelta(days=30)
        return Event.objects.filter(start_date__gte=cutoff_date).order_by('start_date')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class MinistrySitemap(Sitemap):
    """Sitemap for ministry pages."""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        from ministries.models import Ministry
        return Ministry.objects.filter(is_active=True).order_by('display_order', 'name')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
