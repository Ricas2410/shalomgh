"""
Django settings for church_website project.

Production-ready settings with environment variable support.
"""

import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Site Configuration
SITE_NAME = config('SITE_NAME', default='ShalomGH')
CHURCH_NAME = config('CHURCH_NAME', default='Seventh Day Sabbath Church Of Christ')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@shalomgh.com')

# External URLs
MEMBER_PORTAL_URL = config('MEMBER_PORTAL_URL', default='#')
GIVING_PLATFORM_URL = config('GIVING_PLATFORM_URL', default='#')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'crispy_tailwind',
    'widget_tweaks',
]

LOCAL_APPS = [
    'core',
    'pages',
    'sermons',
    'events',
    'ministries',
    'livestream',
    'custom_admin',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'church_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'core.context_processors.page_images',
            ],
        },
    },
]

WSGI_APPLICATION = 'church_website.wsgi.application'

# Database Configuration
default_database_url = 'sqlite:///' + str(BASE_DIR / 'db.sqlite3')
DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL', default=default_database_url)
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'  # Adjust based on church location
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Caching Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'church-website-cache',
        'TIMEOUT': 300,  # 5 minutes default
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# Crispy Forms configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('ADMIN_EMAIL', default='admin@shalomgh.com')

# Google Maps API
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='')

# Google Analytics and SEO Tools
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')
GOOGLE_TAG_MANAGER_ID = config('GOOGLE_TAG_MANAGER_ID', default='')
GOOGLE_SEARCH_CONSOLE_ID = config('GOOGLE_SEARCH_CONSOLE_ID', default='')
BING_WEBMASTER_ID = config('BING_WEBMASTER_ID', default='')
FACEBOOK_PIXEL_ID = config('FACEBOOK_PIXEL_ID', default='')

# SEO Settings
SITE_ID = 1
USE_THOUSAND_SEPARATOR = True

# Security Settings for Production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Performance Settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Social Media URLs
SOCIAL_MEDIA = {
    'facebook': config('FACEBOOK_URL', default=''),
    'twitter': config('TWITTER_URL', default=''),
    'instagram': config('INSTAGRAM_URL', default=''),
    'youtube': config('YOUTUBE_URL', default=''),
}

# Enhanced security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_PRELOAD = True
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Strict'
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    
    # Additional enterprise security settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_TZ = True
    
    # Rate limiting settings
    RATELIMIT_ENABLE = True
    RATELIMIT_USE_CACHE = 'default'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Enterprise SEO and Performance Settings
SEO_SETTINGS = {
    'SITE_NAME': 'ShalomGH',
    'CHURCH_NAME': 'Seventh Day Sabbath Church Of Christ',
    'CHURCH_ALTERNATE_NAMES': ['Shalom', 'Living Yahweh Sabbath Assemblies'],
    'FOUNDER': 'Apostle Ephraim Kwaku Danso',
    'FORMER_MEMBER': 'Apostle Okoh Agyeman',
    'DENOMINATION': 'Sabbath Church',
    'DEFAULT_META_DESCRIPTION': 'Welcome to Seventh Day Sabbath Church Of Christ (Shalom), founded by Apostle Ephraim Kwaku Danso. Join our vibrant Sabbath church community for worship, fellowship, and spiritual growth.',
    'DEFAULT_META_KEYWORDS': 'Seventh Day Sabbath Church Of Christ, Shalom church, Living Yahweh Sabbath Assemblies, Apostle Ephraim Kwaku Danso, Sabbath church, Christian church Ghana',
    'ENABLE_STRUCTURED_DATA': True,
    'ENABLE_BREADCRUMBS': True,
}

# Performance optimization settings
PERFORMANCE_SETTINGS = {
    'ENABLE_COMPRESSION': True,
    'ENABLE_SMART_CACHING': True,
    'CACHE_TIMEOUT_DEFAULT': 300,
    'CACHE_TIMEOUT_STATIC_PAGES': 3600,
    'ENABLE_IMAGE_OPTIMIZATION': True,
    'ENABLE_LAZY_LOADING': True,
}

# Accessibility settings
ACCESSIBILITY_SETTINGS = {
    'ENABLE_SKIP_LINKS': True,
    'ENABLE_HIGH_CONTRAST': True,
    'ENABLE_REDUCED_MOTION': True,
    'WCAG_COMPLIANCE_LEVEL': 'AA',
    'ENABLE_ARIA_LABELS': True,
}

# Static files versioning for cache busting
STATIC_VERSION = '2.0.0'
CACHE_VERSION = 2

# Additional enterprise settings
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Content Security Policy settings
CSP_SETTINGS = {
    'ENABLE_CSP': not DEBUG,
    'CSP_REPORT_URI': '/csp-report/',
    'CSP_REPORT_ONLY': DEBUG,
}
