"""
Advanced SEO template tags for enterprise-level optimization.
"""
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.text import slugify
from core.models import SiteSetting
import json
import re

register = template.Library()


@register.simple_tag
def meta_description(content=None, max_length=155):
    """Generate optimized meta description with proper length."""
    if not content:
        try:
            site_settings = SiteSetting.get_settings()
            content = site_settings.meta_description
        except:
            content = f"Welcome to Seventh Day Sabbath Church Of Christ (Shalom), founded by Apostle Ephraim Kwaku Danso. Join our vibrant Sabbath church community for worship and spiritual growth."
    
    # Clean and optimize content
    content = re.sub(r'\s+', ' ', content).strip()
    
    if len(content) > max_length:
        # Truncate at word boundary
        truncated = content[:max_length-3]
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:
            content = truncated[:last_space] + '...'
        else:
            content = truncated + '...'
    
    return format_html('<meta name="description" content="{}">', content)


@register.simple_tag
def meta_keywords(keywords=None, category=""):
    """Generate enhanced meta keywords with church-specific terms."""
    base_keywords = [
        "Seventh Day Sabbath Church Of Christ",
        "Shalom church",
        "Living Yahweh Sabbath Assemblies", 
        "Apostle Ephraim Kwaku Danso",
        "Sabbath church",
        "Christian church Ghana",
        "worship service",
        "Bible study",
        "prayer meeting"
    ]
    
    if not keywords:
        try:
            site_settings = SiteSetting.get_settings()
            keywords = site_settings.meta_keywords
        except:
            keywords = ""
    
    # Add category-specific keywords
    category_keywords = {
        'sermon': ['sermon', 'preaching', 'Bible teaching', 'spiritual message'],
        'event': ['church event', 'fellowship', 'conference', 'crusade'],
        'ministry': ['ministry', 'church service', 'volunteer', 'outreach'],
        'about': ['church history', 'beliefs', 'leadership', 'vision']
    }
    
    if category in category_keywords:
        base_keywords.extend(category_keywords[category])
    
    if keywords:
        all_keywords = base_keywords + [k.strip() for k in keywords.split(',')]
    else:
        all_keywords = base_keywords
    
    # Remove duplicates and limit
    unique_keywords = list(dict.fromkeys(all_keywords))[:20]
    
    return format_html('<meta name="keywords" content="{}">', ', '.join(unique_keywords))


@register.simple_tag
def canonical_url(request, path=None):
    """Generate canonical URL with proper formatting."""
    if path:
        url = request.build_absolute_uri(path)
    else:
        url = request.build_absolute_uri()
    
    # Ensure URL ends without trailing slash for consistency (except root)
    if url.endswith('/') and len(url.split('/')) > 4:
        url = url.rstrip('/')
    
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
    """Generate enhanced organization structured data for Seventh Day Sabbath Church."""
    try:
        site_settings = SiteSetting.get_settings()
        
        data = {
            "@context": "https://schema.org",
            "@type": "Church",
            "name": "Seventh Day Sabbath Church Of Christ",
            "alternateName": ["Shalom", "Living Yahweh Sabbath Assemblies", "ShalomGH"],
            "description": "A vibrant Sabbath church community founded by Apostle Ephraim Kwaku Danso, serving God and our community through worship, fellowship, and spiritual growth.",
            "founder": {
                "@type": "Person",
                "name": "Apostle Ephraim Kwaku Danso",
                "jobTitle": "Founder and General Overseer"
            },
            "address": {
                "@type": "PostalAddress",
                "streetAddress": getattr(site_settings, 'address', None) or "Church Address",
                "addressLocality": "Accra",
                "addressRegion": "Greater Accra",
                "addressCountry": "Ghana"
            },
            "telephone": getattr(site_settings, 'phone', None) or "+233 XX XXX XXXX",
            "email": getattr(site_settings, 'email', None) or "info@shalomgh.com",
            "denomination": "Sabbath Church",
            "foundingDate": "1990",  # Adjust based on actual founding date
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
