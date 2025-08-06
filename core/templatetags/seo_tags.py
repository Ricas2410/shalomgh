"""
Template tags for SEO optimization.
"""
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings
from core.models import SiteSetting
import json

register = template.Library()


@register.simple_tag
def meta_description(content=None, max_length=160):
    """Generate meta description with proper length."""
    if not content:
        try:
            site_settings = SiteSetting.get_settings()
            content = site_settings.meta_description
        except:
            content = f"Welcome to {getattr(settings, 'CHURCH_NAME', 'Our Church')}, a vibrant community of faith."
    
    if len(content) > max_length:
        content = content[:max_length-3] + '...'
    
    return format_html('<meta name="description" content="{}">', content)


@register.simple_tag
def meta_keywords(keywords=None):
    """Generate meta keywords."""
    if not keywords:
        try:
            site_settings = SiteSetting.get_settings()
            keywords = site_settings.meta_keywords
        except:
            keywords = "church, faith, community, worship, sermons, events, ministry"
    
    return format_html('<meta name="keywords" content="{}">', keywords)


@register.simple_tag
def canonical_url(request, path=None):
    """Generate canonical URL."""
    if path:
        url = request.build_absolute_uri(path)
    else:
        url = request.build_absolute_uri()
    
    return format_html('<link rel="canonical" href="{}">', url)


@register.simple_tag
def og_image(image_url=None, request=None):
    """Generate Open Graph image URL."""
    if not image_url:
        image_url = '/static/img/og-image.jpg'
    
    if request and not image_url.startswith('http'):
        image_url = request.build_absolute_uri(image_url)
    
    return image_url


@register.simple_tag
def structured_data_organization(request=None):
    """Generate organization structured data."""
    try:
        site_settings = SiteSetting.get_settings()
        
        data = {
            "@context": "https://schema.org",
            "@type": "Church",
            "name": getattr(settings, 'CHURCH_NAME', 'Our Church'),
            "alternateName": getattr(settings, 'SITE_NAME', 'Church Website'),
            "description": site_settings.meta_description or "A vibrant community of faith",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": site_settings.address or "123 Church Street",
                "addressLocality": "Accra",
                "addressRegion": "Greater Accra",
                "addressCountry": "Ghana"
            },
            "telephone": site_settings.phone or "+233 XX XXX XXXX",
            "email": site_settings.email or "info@church.com",
        }
        
        if request:
            data["url"] = request.build_absolute_uri('/')
            data["logo"] = request.build_absolute_uri('/static/img/logo.png')
            data["image"] = request.build_absolute_uri('/static/img/og-image.jpg')
        
        # Add social media URLs
        social_urls = []
        if site_settings.facebook_url:
            social_urls.append(site_settings.facebook_url)
        if site_settings.twitter_url:
            social_urls.append(site_settings.twitter_url)
        if site_settings.instagram_url:
            social_urls.append(site_settings.instagram_url)
        if site_settings.youtube_url:
            social_urls.append(site_settings.youtube_url)
        
        if social_urls:
            data["sameAs"] = social_urls
        
        return mark_safe(f'<script type="application/ld+json">{json.dumps(data, indent=2)}</script>')
    
    except Exception:
        return ""


@register.simple_tag
def breadcrumb_structured_data(breadcrumbs):
    """Generate breadcrumb structured data."""
    if not breadcrumbs:
        return ""
    
    items = []
    for i, (name, url) in enumerate(breadcrumbs, 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, indent=2)}</script>')


@register.filter
def truncate_words_seo(value, max_words=25):
    """Truncate text for SEO purposes."""
    if not value:
        return ""
    
    words = value.split()
    if len(words) <= max_words:
        return value
    
    return ' '.join(words[:max_words]) + '...'


@register.simple_tag
def preload_resource(href, resource_type="style", crossorigin=None):
    """Generate resource preload link."""
    attrs = f'rel="preload" href="{href}" as="{resource_type}"'
    
    if crossorigin:
        attrs += f' crossorigin="{crossorigin}"'
    
    return format_html('<link {}>', mark_safe(attrs))


@register.simple_tag
def dns_prefetch(domain):
    """Generate DNS prefetch link."""
    return format_html('<link rel="dns-prefetch" href="//{}">', domain)


@register.simple_tag
def preconnect(url, crossorigin=False):
    """Generate preconnect link."""
    attrs = f'rel="preconnect" href="{url}"'
    if crossorigin:
        attrs += ' crossorigin'
    
    return format_html('<link {}>', mark_safe(attrs))


@register.inclusion_tag('seo/meta_tags.html', takes_context=True)
def render_meta_tags(context, title=None, description=None, keywords=None, image=None):
    """Render complete meta tags."""
    request = context.get('request')

    return {
        'title': title,
        'description': description,
        'keywords': keywords,
        'image': image,
        'request': request,
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Church Website'),
        'CHURCH_NAME': getattr(settings, 'CHURCH_NAME', 'Our Church'),
    }


@register.simple_tag
def lazy_image(src, alt="", css_class="", width=None, height=None, loading="lazy"):
    """Generate lazy-loaded image with proper attributes."""
    attrs = [
        f'src="{src}"',
        f'alt="{alt}"',
        f'loading="{loading}"',
    ]

    if css_class:
        attrs.append(f'class="{css_class}"')

    if width:
        attrs.append(f'width="{width}"')

    if height:
        attrs.append(f'height="{height}"')

    # Add decoding attribute for better performance
    attrs.append('decoding="async"')

    return format_html('<img {}>', mark_safe(' '.join(attrs)))


@register.simple_tag
def responsive_image(src, alt="", css_class="", sizes="100vw"):
    """Generate responsive image with srcset."""
    # This is a simplified version - in production you'd generate multiple sizes
    attrs = [
        f'src="{src}"',
        f'alt="{alt}"',
        f'sizes="{sizes}"',
        'loading="lazy"',
        'decoding="async"',
    ]

    if css_class:
        attrs.append(f'class="{css_class}"')

    return format_html('<img {}>', mark_safe(' '.join(attrs)))
