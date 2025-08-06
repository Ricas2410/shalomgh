"""
Custom Django admin configuration for ShalomGH Church Management System.
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings


class ShalomGHAdminSite(AdminSite):
    """Custom admin site for ShalomGH Church Management System."""
    
    # Site header and title
    site_header = 'ShalomGH Church Admin'
    site_title = 'ShalomGH Admin'
    index_title = 'Church Management System'
    
    # Custom styling
    def each_context(self, request):
        """Add custom context variables to admin templates."""
        context = super().each_context(request)
        context.update({
            'site_url': getattr(settings, 'SITE_URL', '/'),
            'church_name': 'ShalomGH',
            'custom_admin_url': reverse('custom_admin:dashboard'),
        })
        return context


# Create custom admin site instance
admin_site = ShalomGHAdminSite(name='shalomgh_admin')

# Override default admin site
admin.site = admin_site
admin.sites.site = admin_site
