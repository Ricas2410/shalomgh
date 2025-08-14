"""
Advanced SEO utilities for enterprise-level optimization.
"""
import re
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.urls import reverse
from urllib.parse import urljoin


class SEOOptimizer:
    """Advanced SEO optimization utilities."""
    
    @staticmethod
    def generate_meta_description(content, max_length=155):
        """Generate optimized meta description from content."""
        if not content:
            return f"Welcome to {settings.CHURCH_NAME}, a vibrant Sabbath church community founded by Apostle Ephraim Kwaku Danso. Join us for worship, fellowship, and spiritual growth."
        
        # Strip HTML tags and clean content
        clean_content = strip_tags(content)
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        if len(clean_content) <= max_length:
            return clean_content
        
        # Truncate at word boundary
        truncated = clean_content[:max_length]
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:  # Only truncate at word if close to end
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    @staticmethod
    def generate_keywords(title="", content="", category=""):
        """Generate SEO keywords based on content and church context."""
        base_keywords = [
            "Seventh Day Sabbath Church Of Christ",
            "Shalom church",
            "Living Yahweh Sabbath Assemblies",
            "Apostle Ephraim Kwaku Danso",
            "Sabbath church",
            "Christian church",
            "Ghana church",
            "worship service",
            "Bible study",
            "prayer meeting",
            "church community"
        ]
        
        # Add category-specific keywords
        category_keywords = {
            'sermon': ['sermon', 'preaching', 'Bible teaching', 'spiritual message', 'word of God'],
            'event': ['church event', 'fellowship', 'conference', 'crusade', 'convention'],
            'ministry': ['ministry', 'church service', 'volunteer', 'outreach', 'missions'],
            'about': ['church history', 'beliefs', 'leadership', 'vision', 'mission'],
        }
        
        if category in category_keywords:
            base_keywords.extend(category_keywords[category])
        
        # Extract keywords from title and content
        if title:
            title_words = [word.lower() for word in re.findall(r'\b\w+\b', title) if len(word) > 3]
            base_keywords.extend(title_words[:5])
        
        if content:
            content_words = [word.lower() for word in re.findall(r'\b\w+\b', strip_tags(content)) if len(word) > 4]
            # Get most common words (simple frequency)
            word_freq = {}
            for word in content_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            base_keywords.extend([word for word, _ in top_words])
        
        # Remove duplicates and return as comma-separated string
        unique_keywords = list(dict.fromkeys(base_keywords))
        return ", ".join(unique_keywords[:20])  # Limit to 20 keywords
    
    @staticmethod
    def generate_structured_data(page_type, **kwargs):
        """Generate JSON-LD structured data for different page types."""
        base_org = {
            "@context": "https://schema.org",
            "@type": "Church",
            "name": "Seventh Day Sabbath Church Of Christ",
            "alternateName": ["Shalom", "Living Yahweh Sabbath Assemblies"],
            "description": "A vibrant Sabbath church community founded by Apostle Ephraim Kwaku Danso, serving God and our community through worship, fellowship, and spiritual growth.",
            "founder": {
                "@type": "Person",
                "name": "Apostle Ephraim Kwaku Danso"
            },
            "url": settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else "",
            "sameAs": [
                settings.SOCIAL_MEDIA.get('facebook', ''),
                settings.SOCIAL_MEDIA.get('twitter', ''),
                settings.SOCIAL_MEDIA.get('instagram', ''),
                settings.SOCIAL_MEDIA.get('youtube', ''),
            ]
        }
        
        if page_type == 'organization':
            return base_org
        
        elif page_type == 'sermon':
            return {
                "@context": "https://schema.org",
                "@type": "VideoObject",
                "name": kwargs.get('title', ''),
                "description": kwargs.get('description', ''),
                "uploadDate": kwargs.get('date', ''),
                "duration": kwargs.get('duration', ''),
                "contentUrl": kwargs.get('video_url', ''),
                "thumbnailUrl": kwargs.get('thumbnail', ''),
                "publisher": base_org
            }
        
        elif page_type == 'event':
            return {
                "@context": "https://schema.org",
                "@type": "Event",
                "name": kwargs.get('title', ''),
                "description": kwargs.get('description', ''),
                "startDate": kwargs.get('start_date', ''),
                "endDate": kwargs.get('end_date', ''),
                "location": {
                    "@type": "Place",
                    "name": kwargs.get('location_name', ''),
                    "address": kwargs.get('address', '')
                },
                "organizer": base_org
            }
        
        elif page_type == 'webpage':
            return {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": kwargs.get('title', ''),
                "description": kwargs.get('description', ''),
                "url": kwargs.get('url', ''),
                "isPartOf": {
                    "@type": "WebSite",
                    "name": settings.CHURCH_NAME if hasattr(settings, 'CHURCH_NAME') else "ShalomGH",
                    "url": settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else ""
                },
                "about": base_org
            }
        
        return base_org


def get_page_seo_data(request, title="", description="", keywords="", image="", page_type="webpage", **kwargs):
    """Get comprehensive SEO data for a page."""
    optimizer = SEOOptimizer()
    
    # Generate optimized meta description if not provided
    if not description and 'content' in kwargs:
        description = optimizer.generate_meta_description(kwargs['content'])
    elif not description:
        description = f"Welcome to {settings.CHURCH_NAME}, a vibrant Sabbath church community founded by Apostle Ephraim Kwaku Danso."
    
    # Generate keywords if not provided
    if not keywords:
        keywords = optimizer.generate_keywords(title, kwargs.get('content', ''), kwargs.get('category', ''))
    
    # Build absolute URLs
    canonical_url = request.build_absolute_uri()
    if image and not image.startswith('http'):
        image = request.build_absolute_uri(image)
    
    # Generate structured data
    structured_data = optimizer.generate_structured_data(page_type, 
                                                       title=title, 
                                                       description=description,
                                                       url=canonical_url,
                                                       **kwargs)
    
    return {
        'title': title,
        'description': description,
        'keywords': keywords,
        'canonical_url': canonical_url,
        'og_image': image,
        'structured_data': structured_data,
    }
