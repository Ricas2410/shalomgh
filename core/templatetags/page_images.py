"""
Template tags for page images functionality.
"""
from django import template
from core.models import PageImage

register = template.Library()


@register.simple_tag
def get_page_image_url(section, index=0, fallback_url=''):
    """
    Get image URL for a specific page section with fallback.
    
    Usage: {% get_page_image_url "home_hero" 0 "fallback_url" %}
    """
    try:
        images = PageImage.objects.filter(
            page_section=section, 
            is_active=True
        ).order_by('display_order')
        
        if images.exists() and len(images) > index:
            return images[index].get_image_url()
        
        return fallback_url
    except:
        return fallback_url


@register.inclusion_tag('core/partials/page_image.html')
def page_image(section, index=0, fallback_url='', alt_text='', css_class=''):
    """
    Render a page image with proper fallback.
    
    Usage: {% page_image "home_hero" 0 "fallback_url" "Alt text" "css-class" %}
    """
    try:
        images = PageImage.objects.filter(
            page_section=section, 
            is_active=True
        ).order_by('display_order')
        
        image_obj = None
        image_url = fallback_url
        
        if images.exists() and len(images) > index:
            image_obj = images[index]
            image_url = image_obj.get_image_url()
            if not alt_text and image_obj.alt_text:
                alt_text = image_obj.alt_text
        
        return {
            'image_url': image_url,
            'alt_text': alt_text,
            'css_class': css_class,
            'image_obj': image_obj,
        }
    except:
        return {
            'image_url': fallback_url,
            'alt_text': alt_text,
            'css_class': css_class,
            'image_obj': None,
        }
