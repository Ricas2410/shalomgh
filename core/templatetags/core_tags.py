from django import template
from ..models import SiteSetting, ServiceTime

register = template.Library()


@register.simple_tag
def get_site_settings():
    """Get the site settings object."""
    try:
        return SiteSetting.objects.get(pk=1)
    except SiteSetting.DoesNotExist:
        return None


@register.simple_tag
def get_service_times():
    """Get all active service times ordered by display order."""
    return ServiceTime.objects.filter(is_active=True).order_by('display_order', 'day')


@register.inclusion_tag('core/service_times_display.html')
def display_service_times():
    """Display service times in a formatted way."""
    service_times = ServiceTime.objects.filter(is_active=True).order_by('display_order', 'day')
    return {'service_times': service_times}
