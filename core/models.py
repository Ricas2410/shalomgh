"""
Core models for site-wide settings and configurations.
"""
from django.db import models
from django.core.validators import EmailValidator, URLValidator
from PIL import Image
import os


class SiteSetting(models.Model):
    """Model for storing site-wide settings."""

    # Site Information
    site_name = models.CharField(max_length=100, default='ShalomGH')
    church_name = models.CharField(max_length=200, default='Seventh Day Sabbath Church Of Christ')
    tagline = models.CharField(max_length=200, blank=True)
    welcome_message = models.TextField(blank=True)

    # Hero Section
    hero_title = models.CharField(
        max_length=200,
        blank=True,
        default='Welcome to Our Church Family',
        help_text='Main title displayed on the homepage hero section'
    )
    hero_subtitle = models.TextField(
        blank=True,
        default='Join our vibrant community of believers as we worship, grow in faith, and serve with purpose in God\'s amazing love.',
        help_text='Subtitle/description displayed below the hero title'
    )

    # Contact Information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(validators=[EmailValidator()], blank=True)
    address = models.TextField(blank=True)

    # Service Times
    service_times = models.TextField(
        blank=True,
        help_text="Enter service times in HTML format"
    )

    # External URLs
    member_portal_url = models.URLField(
        validators=[URLValidator()],
        blank=True,
        help_text="URL to external member portal"
    )
    giving_platform_url = models.URLField(
        validators=[URLValidator()],
        blank=True,
        help_text="URL to external giving platform"
    )

    # Payment Configuration
    paystack_public_key = models.CharField(
        max_length=100,
        blank=True,
        help_text="Paystack public key for online donations"
    )
    paystack_secret_key = models.CharField(
        max_length=100,
        blank=True,
        help_text="Paystack secret key (keep this secure)"
    )
    enable_paystack = models.BooleanField(
        default=False,
        help_text="Enable Paystack payment integration"
    )

    # Social Media
    facebook_url = models.URLField(validators=[URLValidator()], blank=True)
    twitter_url = models.URLField(validators=[URLValidator()], blank=True)
    instagram_url = models.URLField(validators=[URLValidator()], blank=True)
    youtube_url = models.URLField(validators=[URLValidator()], blank=True)

    # SEO Settings
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Meta description for SEO (max 160 characters)"
    )
    meta_keywords = models.TextField(
        blank=True,
        help_text="Comma-separated keywords for SEO"
    )

    # Google Services
    google_maps_api_key = models.CharField(max_length=100, blank=True)
    google_analytics_id = models.CharField(max_length=20, blank=True)

    # CTA Section Media
    cta_image = models.ImageField(
        upload_to='cta_images/',
        blank=True,
        null=True,
        help_text="Image to display in CTA sections (optional)"
    )
    cta_youtube_url = models.URLField(
        validators=[URLValidator()],
        blank=True,
        help_text="YouTube video URL to embed in CTA sections (optional)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.site_name} Settings"

    @classmethod
    def get_settings(cls):
        """Get or create site settings."""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class ServiceTime(models.Model):
    """Model for managing church service times."""

    name = models.CharField(
        max_length=100,
        help_text="Name of the service (e.g., 'Saturday Sabbath Worship')"
    )
    time = models.CharField(
        max_length=50,
        help_text="Time of the service (e.g., '10:00 AM - 12:00 PM')"
    )
    day = models.CharField(
        max_length=20,
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ],
        help_text="Day of the week for this service"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which to display this service (lower numbers first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this service time should be displayed"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Time"
        verbose_name_plural = "Service Times"
        ordering = ['display_order', 'day']

    def __str__(self):
        return f"{self.name} - {self.time}"


class ContactMessage(models.Model):
    """Model for storing contact form submissions."""

    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=200)
    message = models.TextField()
    phone = models.CharField(max_length=20, blank=True)

    # Status tracking
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class KeyMilestone(models.Model):
    """Model for storing key milestones/achievements displayed on the contact page."""

    title = models.CharField(
        max_length=100,
        help_text="Title of the milestone (e.g., 'Years of Service', 'Members Served')"
    )
    value = models.CharField(
        max_length=20,
        help_text="The milestone value (e.g., '25+', '1000+', '50')"
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional description of the milestone"
    )
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="CSS class for icon (e.g., 'fas fa-church', 'fas fa-users')"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which to display the milestone (lower numbers first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether to display this milestone on the website"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Key Milestone"
        verbose_name_plural = "Key Milestones"
        ordering = ['display_order', 'title']

    def __str__(self):
        return f"{self.title}: {self.value}"


class PageImage(models.Model):
    """Model for managing images used across different pages."""

    PAGE_CHOICES = [
        ('home_hero', 'Home Page Hero Background'),
        ('home_welcome', 'Home Page Welcome Section'),
        ('about_hero', 'About Page Hero Background'),
        ('about_team', 'About Page Team Section'),
        ('sermons_hero', 'Sermons Page Hero Background'),
        ('events_hero', 'Events Page Hero Background'),
        ('ministries_hero', 'Ministries Page Hero Background'),
        ('contact_hero', 'Contact Page Hero Background'),
        ('giving_hero', 'Giving Page Hero Background'),
        ('plan_visit_hero', 'Plan Visit Page Hero Background'),
        ('beliefs_hero', 'Beliefs Page Hero Background'),
        ('leadership_hero', 'Leadership Page Hero Background'),
        ('location_hero', 'Location Page Hero Background'),
        ('speakers_hero', 'Speakers Page Hero Background'),
        ('series_hero', 'Sermon Series Page Hero Background'),
        ('general_church', 'General Church Photos'),
        ('worship_service', 'Worship Service Photos'),
        ('community_events', 'Community Events Photos'),
        ('youth_ministry', 'Youth Ministry Photos'),
        ('children_ministry', 'Children Ministry Photos'),
        ('music_ministry', 'Music Ministry Photos'),
    ]

    page_section = models.CharField(
        max_length=50,
        choices=PAGE_CHOICES,
        help_text="Select which page/section this image is for"
    )
    title = models.CharField(
        max_length=200,
        help_text="Descriptive title for the image"
    )
    image = models.ImageField(
        upload_to='page_images/',
        help_text="Upload image (recommended: 1920x1080 for hero images, 800x600 for section images)"
    )
    fallback_url = models.URLField(
        blank=True,
        help_text="Fallback image URL (e.g., from Unsplash) if uploaded image is not available"
    )
    alt_text = models.CharField(
        max_length=200,
        help_text="Alternative text for accessibility"
    )
    caption = models.TextField(
        blank=True,
        help_text="Optional caption for the image"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order for displaying multiple images in the same section"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this image should be displayed"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Page Image"
        verbose_name_plural = "Page Images"
        ordering = ['page_section', 'display_order', '-created_at']
        unique_together = ['page_section', 'display_order']

    def __str__(self):
        return f"{self.get_page_section_display()} - {self.title}"

    def get_image_url(self):
        """Get the image URL, falling back to fallback_url if image is not available."""
        if self.image and hasattr(self.image, 'url'):
            try:
                return self.image.url
            except:
                pass
        return self.fallback_url if self.fallback_url else ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize image if it exists and is too large
        if self.image and hasattr(self.image, 'path'):
            try:
                img = Image.open(self.image.path)
                # Resize hero images to max 1920x1080
                if 'hero' in self.page_section and (img.height > 1080 or img.width > 1920):
                    output_size = (1920, 1080)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                    img.save(self.image.path, optimize=True, quality=85)
                # Resize other images to max 800x600
                elif 'hero' not in self.page_section and (img.height > 600 or img.width > 800):
                    output_size = (800, 600)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                    img.save(self.image.path, optimize=True, quality=85)
            except Exception as e:
                pass  # Silently handle image processing errors
