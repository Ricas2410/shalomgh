"""
Advanced performance optimization utilities for enterprise-level speed.
"""
import gzip
import time
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.cache import get_cache_key
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import logging

logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """Advanced performance optimization utilities."""
    
    @staticmethod
    def compress_response(response):
        """Compress response content for faster delivery."""
        if response.get('Content-Encoding') == 'gzip':
            return response
        
        content = response.content
        if len(content) < 200:  # Don't compress very small responses
            return response
        
        compressed_content = gzip.compress(content)
        if len(compressed_content) >= len(content):  # No benefit
            return response
        
        response.content = compressed_content
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = str(len(compressed_content))
        
        return response
    
    @staticmethod
    def generate_etag(content):
        """Generate ETag for caching."""
        import hashlib
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    @staticmethod
    def smart_cache_key(request, prefix=''):
        """Generate intelligent cache key based on request."""
        key_parts = [prefix, request.path]
        
        # Include relevant query parameters
        relevant_params = ['page', 'category', 'tag', 'search']
        for param in relevant_params:
            if param in request.GET:
                key_parts.append(f"{param}_{request.GET[param]}")
        
        # Include user-specific data if authenticated (safely check for user attribute)
        if hasattr(request, 'user') and request.user.is_authenticated:
            key_parts.append(f"user_{request.user.id}")
        
        return "_".join(key_parts)


class SmartCacheMiddleware:
    """Intelligent caching middleware with dynamic TTL."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_settings = {
            '/': 300,  # Home page - 5 minutes
            '/sermons/': 600,  # Sermons - 10 minutes
            '/events/': 300,  # Events - 5 minutes
            '/about/': 3600,  # About - 1 hour
            '/contact/': 1800,  # Contact - 30 minutes
            '/ministries/': 1800,  # Ministries - 30 minutes
        }
    
    def __call__(self, request):
        # Check cache first
        cache_key = PerformanceOptimizer.smart_cache_key(request, 'page')
        cached_response = cache.get(cache_key)
        
        if cached_response and not settings.DEBUG:
            cached_response['X-Cache'] = 'HIT'
            return cached_response
        
        # Get response
        response = self.get_response(request)
        
        # Cache successful GET requests
        if (request.method == 'GET' and 
            response.status_code == 200 and 
            not (hasattr(request, 'user') and request.user.is_authenticated)):
            
            # Determine cache timeout
            timeout = self.get_cache_timeout(request.path)
            
            if timeout > 0:
                cache.set(cache_key, response, timeout)
                response['X-Cache'] = 'MISS'
                response['Cache-Control'] = f'public, max-age={timeout}'
        
        return response
    
    def get_cache_timeout(self, path):
        """Get cache timeout for specific path."""
        for pattern, timeout in self.cache_settings.items():
            if path.startswith(pattern):
                return timeout
        return 0  # Don't cache by default


class ImageOptimizationMiddleware:
    """Middleware for image optimization and WebP serving."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add WebP support headers
        if 'image/' in response.get('Content-Type', ''):
            accept_header = request.META.get('HTTP_ACCEPT', '')
            if 'image/webp' in accept_header:
                response['Vary'] = 'Accept'
        
        return response


def performance_monitoring_middleware(get_response):
    """Middleware to monitor page performance."""
    
    def middleware(request):
        start_time = time.time()
        
        response = get_response(request)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Add performance headers
        response['X-Response-Time'] = f"{response_time:.3f}s"
        
        # Log slow requests
        if response_time > 2.0:  # Log requests taking more than 2 seconds
            logger.warning(
                f"Slow request: {request.method} {request.path} took {response_time:.3f}s"
            )
        
        return response
    
    return middleware


class DatabaseOptimizer:
    """Database query optimization utilities."""
    
    @staticmethod
    def optimize_queryset(queryset, select_related=None, prefetch_related=None):
        """Optimize queryset with proper select_related and prefetch_related."""
        if select_related:
            queryset = queryset.select_related(*select_related)
        
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        
        return queryset
    
    @staticmethod
    def get_or_cache(model, cache_key, **kwargs):
        """Get object from cache or database."""
        obj = cache.get(cache_key)
        if obj is None:
            try:
                obj = model.objects.get(**kwargs)
                cache.set(cache_key, obj, 3600)  # Cache for 1 hour
            except model.DoesNotExist:
                return None
        return obj


# Decorators for view optimization
def smart_cache_view(timeout=300, vary_on=None):
    """Smart caching decorator for views."""
    def decorator(view_func):
        if vary_on:
            view_func = vary_on_headers(*vary_on)(view_func)
        return cache_page(timeout)(view_func)
    return decorator


def compress_view(view_func):
    """Decorator to compress view responses."""
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return PerformanceOptimizer.compress_response(response)
        return response
    return wrapper


# Context processor for performance data
def performance_context(request):
    """Add performance-related context variables."""
    return {
        'ENABLE_COMPRESSION': not settings.DEBUG,
        'CACHE_VERSION': getattr(settings, 'CACHE_VERSION', 1),
        'STATIC_VERSION': getattr(settings, 'STATIC_VERSION', '1.0'),
    }
