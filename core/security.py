"""
Enhanced security utilities for enterprise-level protection.
"""
import hashlib
import secrets
from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class SecurityEnforcer:
    """Advanced security enforcement utilities."""
    
    @staticmethod
    def generate_csp_header():
        """Generate Content Security Policy header for enhanced security."""
        # Generate nonce for inline scripts
        nonce = secrets.token_urlsafe(16)
        
        csp_directives = [
            "default-src 'self'",
            f"script-src 'self' 'nonce-{nonce}' https://www.google-analytics.com https://www.googletagmanager.com https://fonts.googleapis.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: https: blob:",
            "media-src 'self' https:",
            "connect-src 'self' https://www.google-analytics.com",
            "frame-src 'self' https://www.youtube.com https://www.google.com",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
        ]
        
        return "; ".join(csp_directives), nonce
    
    @staticmethod
    def rate_limit_check(request, action='general', limit=60, window=3600):
        """
        Advanced rate limiting with different limits for different actions.
        
        Args:
            request: Django request object
            action: Type of action (e.g., 'contact_form', 'search', 'general')
            limit: Number of allowed requests
            window: Time window in seconds
        """
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Create cache key
        cache_key = f"rate_limit:{action}:{ip}"
        
        # Get current count
        current_count = cache.get(cache_key, 0)
        
        if current_count >= limit:
            logger.warning(f"Rate limit exceeded for IP {ip} on action {action}")
            return False
        
        # Increment counter
        cache.set(cache_key, current_count + 1, window)
        return True
    
    @staticmethod
    def validate_file_upload(uploaded_file, allowed_types=None, max_size=10*1024*1024):
        """
        Validate uploaded files for security.
        
        Args:
            uploaded_file: Django UploadedFile object
            allowed_types: List of allowed MIME types
            max_size: Maximum file size in bytes
        """
        if allowed_types is None:
            allowed_types = [
                'image/jpeg', 'image/png', 'image/gif', 'image/webp',
                'audio/mpeg', 'audio/wav', 'audio/ogg',
                'video/mp4', 'video/webm', 'video/ogg',
                'application/pdf'
            ]
        
        # Check file size
        if uploaded_file.size > max_size:
            return False, "File size exceeds maximum allowed size"
        
        # Check MIME type
        if uploaded_file.content_type not in allowed_types:
            return False, "File type not allowed"
        
        # Check file extension matches MIME type
        extension_map = {
            'image/jpeg': ['.jpg', '.jpeg'],
            'image/png': ['.png'],
            'image/gif': ['.gif'],
            'image/webp': ['.webp'],
            'audio/mpeg': ['.mp3'],
            'audio/wav': ['.wav'],
            'audio/ogg': ['.ogg'],
            'video/mp4': ['.mp4'],
            'video/webm': ['.webm'],
            'video/ogg': ['.ogv'],
            'application/pdf': ['.pdf']
        }
        
        file_extension = uploaded_file.name.lower().split('.')[-1]
        if f'.{file_extension}' not in extension_map.get(uploaded_file.content_type, []):
            return False, "File extension doesn't match content type"
        
        return True, "File is valid"
    
    @staticmethod
    def generate_secure_token(length=32):
        """Generate cryptographically secure token."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_sensitive_data(data, salt=None):
        """Hash sensitive data with salt."""
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # Use PBKDF2 for key derivation
        from django.contrib.auth.hashers import PBKDF2PasswordHasher
        hasher = PBKDF2PasswordHasher()
        return hasher.encode(data, salt)


def security_headers_middleware(get_response):
    """Middleware to add comprehensive security headers."""
    
    def middleware(request):
        response = get_response(request)
        
        # Generate CSP header
        csp_header, nonce = SecurityEnforcer.generate_csp_header()
        
        # Add security headers
        security_headers = {
            'Content-Security-Policy': csp_header,
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        }
        
        for header, value in security_headers.items():
            response[header] = value
        
        # Store nonce in request for template use
        request.csp_nonce = nonce
        
        return response
    
    return middleware


class BruteForceProtection:
    """Protection against brute force attacks."""
    
    @staticmethod
    def check_login_attempts(ip_address, max_attempts=5, lockout_time=1800):
        """
        Check if IP should be locked out due to failed login attempts.
        
        Args:
            ip_address: Client IP address
            max_attempts: Maximum failed attempts before lockout
            lockout_time: Lockout duration in seconds
        """
        cache_key = f"login_attempts:{ip_address}"
        attempts = cache.get(cache_key, {'count': 0, 'first_attempt': None})
        
        # Check if currently locked out
        if attempts['count'] >= max_attempts:
            if attempts.get('lockout_until'):
                if timezone.now() < attempts['lockout_until']:
                    return False, f"Account locked. Try again later."
        
        return True, "OK"
    
    @staticmethod
    def record_failed_attempt(ip_address, max_attempts=5, lockout_time=1800):
        """Record a failed login attempt."""
        cache_key = f"login_attempts:{ip_address}"
        attempts = cache.get(cache_key, {'count': 0, 'first_attempt': timezone.now()})
        
        attempts['count'] += 1
        attempts['last_attempt'] = timezone.now()
        
        if attempts['count'] >= max_attempts:
            attempts['lockout_until'] = timezone.now() + timedelta(seconds=lockout_time)
            logger.warning(f"IP {ip_address} locked out due to {max_attempts} failed login attempts")
        
        cache.set(cache_key, attempts, lockout_time)
    
    @staticmethod
    def clear_attempts(ip_address):
        """Clear failed attempts for successful login."""
        cache_key = f"login_attempts:{ip_address}"
        cache.delete(cache_key)
