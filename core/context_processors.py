"""
Context processors for making site-wide settings and data available in templates.
"""
from django.conf import settings
from .models import SiteSetting, PageImage


def site_settings(request):
    """
    Add site-wide settings to template context.
    """
    try:
        site_settings_obj = SiteSetting.get_settings()
        return {
            'site_settings': site_settings_obj,
            'SITE_NAME': site_settings_obj.site_name,
            'CHURCH_NAME': site_settings_obj.church_name,
            'MEMBER_PORTAL_URL': site_settings_obj.member_portal_url or '#',
            'GIVING_PLATFORM_URL': site_settings_obj.giving_platform_url or '#',
            'SOCIAL_MEDIA': {
                'facebook': site_settings_obj.facebook_url,
                'twitter': site_settings_obj.twitter_url,
                'instagram': site_settings_obj.instagram_url,
                'youtube': site_settings_obj.youtube_url,
            },
            'GOOGLE_MAPS_API_KEY': site_settings_obj.google_maps_api_key,
            'GOOGLE_ANALYTICS_ID': site_settings_obj.google_analytics_id,
            'CTA_IMAGE': site_settings_obj.cta_image,
            'CTA_YOUTUBE_URL': site_settings_obj.cta_youtube_url,
        }
    except:
        # Fallback to Django settings if database is not available
        return {
            'site_settings': None,
            'SITE_NAME': getattr(settings, 'SITE_NAME', 'ShalomGH'),
            'CHURCH_NAME': getattr(settings, 'CHURCH_NAME', 'Seventh Day Sabbath Church Of Christ'),
            'MEMBER_PORTAL_URL': getattr(settings, 'MEMBER_PORTAL_URL', '#'),
            'GIVING_PLATFORM_URL': getattr(settings, 'GIVING_PLATFORM_URL', '#'),
            'SOCIAL_MEDIA': getattr(settings, 'SOCIAL_MEDIA', {}),
            'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
            'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
        }


def page_images(request):
    """Make page images available in all templates."""
    try:
        # Get all active page images grouped by section
        images = {}
        for image in PageImage.objects.filter(is_active=True).order_by('page_section', 'display_order'):
            section = image.page_section
            if section not in images:
                images[section] = []
            images[section].append(image)

        # Helper function to get image URL with fallback
        def get_page_image_url(section, index=0, fallback_url=''):
            """Get image URL for a specific page section."""
            if section in images and len(images[section]) > index:
                return images[section][index].get_image_url()
            return fallback_url

        return {
            'page_images': images,
            'get_page_image_url': get_page_image_url,
        }
    except:
        # Fallback function if database is not available
        def get_page_image_url(section, index=0, fallback_url=''):
            return fallback_url

        return {
            'page_images': {},
            'get_page_image_url': get_page_image_url,
        }
