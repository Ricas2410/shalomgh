"""
Production settings for Seventh Day Sabbath Church Of Christ (ShalomGH) on Fly.io
Optimized for cost-effective deployment with enterprise features
"""

from .settings import *
import os
import dj_database_url

# Override settings for production
DEBUG = False

# Allowed hosts for Fly.io
ALLOWED_HOSTS = [
    'shalomgh.fly.dev',
    '*.fly.dev',
    'localhost',
    '127.0.0.1',
]

# Database configuration for Fly.io (SQLite for cost efficiency)
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite:///data/db.sqlite3')
    )
}

# Static files configuration for Fly.io
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'data', 'media')

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Trust Fly.io proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Logging configuration for Fly.io
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache configuration (in-memory for single machine)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'shalomgh-cache',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Email configuration for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@shalomgh.fly.dev')

# SEO and Analytics
GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')
GOOGLE_TAG_MANAGER_ID = os.environ.get('GOOGLE_TAG_MANAGER_ID', '')
GOOGLE_SEARCH_CONSOLE_ID = os.environ.get('GOOGLE_SEARCH_CONSOLE_ID', '')
BING_WEBMASTER_ID = os.environ.get('BING_WEBMASTER_ID', '')

# Church-specific production settings
CHURCH_PRODUCTION_SETTINGS = {
    'SITE_URL': 'https://shalomgh.fly.dev',
    'CANONICAL_DOMAIN': 'shalomgh.fly.dev',
    'ENABLE_SEO_OPTIMIZATION': True,
    'ENABLE_STRUCTURED_DATA': True,
    'ENABLE_SITEMAP_PING': True,
}

# Update SEO settings for production
SEO_SETTINGS.update({
    'SITE_URL': 'https://shalomgh.fly.dev',
    'CANONICAL_DOMAIN': 'shalomgh.fly.dev',
})

# Sentry configuration for error monitoring (optional)
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,  # Low rate for cost efficiency
        send_default_pii=False,
        environment='production',
    )

# Performance optimizations for single machine
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# File upload limits (to manage storage costs)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB

# Compress static files
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
