"""
URL configuration for church_website project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from core.sitemaps import (
    StaticViewSitemap, SermonSitemap, SermonSeriesSitemap,
    EventSitemap, MinistrySitemap
)

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'sermons': SermonSitemap,
    'sermon-series': SermonSeriesSitemap,
    'events': EventSitemap,
    'ministries': MinistrySitemap,
}

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    path('my-admin/', include('custom_admin.urls')),

    # Main site URLs
    path('', include('core.urls')),
    path('about/', include('pages.urls')),
    path('sermons/', include('sermons.urls')),
    path('events/', include('events.urls')),
    path('ministries/', include('ministries.urls')),

    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
