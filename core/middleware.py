"""
Custom middleware for performance optimization and security.
"""
from django.utils.cache import patch_cache_control
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import gzip
import io


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses."""
    
    def process_response(self, request, response):
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy (basic)
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
            "https://cdn.tailwindcss.com https://www.googletagmanager.com "
            "https://www.google-analytics.com; "
            "style-src 'self' 'unsafe-inline' "
            "https://fonts.googleapis.com https://cdn.tailwindcss.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://www.google-analytics.com; "
            "frame-src https://www.youtube.com https://www.google.com;"
        )
        
        return response


class CacheControlMiddleware(MiddlewareMixin):
    """Add appropriate cache control headers."""
    
    def process_response(self, request, response):
        # Don't cache admin pages
        if request.path.startswith('/admin/') or request.path.startswith('/my-admin/'):
            patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
            return response
        
        # Cache static files for a long time
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            patch_cache_control(response, max_age=31536000)  # 1 year
            return response
        
        # Cache pages for a shorter time
        if response.status_code == 200:
            if request.path == '/':
                # Home page - cache for 1 hour
                patch_cache_control(response, max_age=3600)
            elif any(request.path.startswith(path) for path in ['/sermons/', '/events/', '/ministries/']):
                # Content pages - cache for 30 minutes
                patch_cache_control(response, max_age=1800)
            else:
                # Other pages - cache for 1 hour
                patch_cache_control(response, max_age=3600)
        
        return response


class CompressionMiddleware(MiddlewareMixin):
    """Compress responses with gzip."""
    
    def process_response(self, request, response):
        # Don't compress if already compressed or if it's not worth it
        if (response.get('Content-Encoding') or 
            response.status_code < 200 or 
            response.status_code >= 300 or
            len(response.content) < 200):
            return response
        
        # Check if client accepts gzip
        accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
        if 'gzip' not in accept_encoding.lower():
            return response
        
        # Compress content types that benefit from compression
        content_type = response.get('Content-Type', '').lower()
        compressible_types = [
            'text/html',
            'text/css',
            'text/javascript',
            'application/javascript',
            'application/json',
            'text/xml',
            'application/xml',
        ]
        
        if not any(ct in content_type for ct in compressible_types):
            return response
        
        try:
            # Compress the content
            compressed_content = gzip.compress(response.content)
            
            # Only use compressed version if it's actually smaller
            if len(compressed_content) < len(response.content):
                response.content = compressed_content
                response['Content-Encoding'] = 'gzip'
                response['Content-Length'] = str(len(compressed_content))
        except Exception:
            # If compression fails, return original response
            pass
        
        return response


class PerformanceMiddleware(MiddlewareMixin):
    """Add performance-related headers and optimizations."""
    
    def process_response(self, request, response):
        # Add performance hints
        if response.status_code == 200:
            # DNS prefetch hints for external resources
            dns_prefetch = [
                'fonts.googleapis.com',
                'fonts.gstatic.com',
                'www.google-analytics.com',
                'www.googletagmanager.com',
            ]
            
            # Add Link headers for DNS prefetch
            for domain in dns_prefetch:
                response['Link'] = f'<///{domain}>; rel=dns-prefetch'
        
        return response
