"""
Models for ministry and group management.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import EmailValidator
from pages.models import LeadershipProfile


class Ministry(models.Model):
    """Model for church ministries and groups."""

    MINISTRY_TYPE_CHOICES = [
        ('mens', "Men's Ministry"),
        ('womens', "Women's Ministry"),
        ('youth', 'Youth & Teens'),
        ('children', "Children's Church"),
        ('music', 'Music & Worship'),
        ('prayer', 'Prayer & Intercession'),
        ('evangelism', 'Evangelism & Missions'),
        ('discipleship', 'Discipleship / Small Groups'),
        ('outreach', 'Community Outreach'),
        ('education', 'Christian Education'),
        ('other', 'Other'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    ministry_type = models.CharField(
        max_length=20,
        choices=MINISTRY_TYPE_CHOICES,
        default='other'
    )

    # Description
    short_description = models.CharField(
        max_length=200,
        help_text="Brief description for ministry listing"
    )
    description = models.TextField()
    mission_statement = models.TextField(blank=True)

    # Leadership
    leader = models.ForeignKey(
        LeadershipProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='led_ministries'
    )
    assistant_leaders = models.ManyToManyField(
        LeadershipProfile,
        blank=True,
        related_name='assisted_ministries'
    )

    # Contact Information
    contact_email = models.EmailField(
        validators=[EmailValidator()],
        blank=True
    )
    contact_phone = models.CharField(max_length=20, blank=True)

    # Meeting Information
    meeting_day = models.CharField(
        max_length=20,
        blank=True,
        help_text="e.g., 'Every Sunday', 'First Friday of the month'"
    )
    meeting_time = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., '10:00 AM - 12:00 PM'"
    )
    meeting_location = models.CharField(max_length=200, blank=True)

    # Age Group (if applicable)
    min_age = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Minimum age for participation"
    )
    max_age = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Maximum age for participation (leave blank for no limit)"
    )

    # Media
    featured_image = models.ImageField(
        upload_to='ministries/',
        blank=True,
        help_text="Recommended size: 800x400 pixels"
    )

    # Activities and Programs
    activities = models.TextField(
        blank=True,
        help_text="List of activities and programs"
    )

    # Requirements
    requirements = models.TextField(
        blank=True,
        help_text="Any requirements for joining this ministry"
    )

    # Display Settings
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Meta description for SEO (max 160 characters)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ministry"
        verbose_name_plural = "Ministries"
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['ministry_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['display_order']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ministries:detail', kwargs={'slug': self.slug})

    def get_age_range_display(self):
        """Get formatted age range display."""
        if self.min_age and self.max_age:
            return f"Ages {self.min_age}-{self.max_age}"
        elif self.min_age:
            return f"Ages {self.min_age}+"
        elif self.max_age:
            return f"Ages up to {self.max_age}"
        return "All Ages"

    def get_leader_name(self):
        """Get the leader's name."""
        if self.leader:
            return self.leader.get_full_name()
        return "TBD"


class MinistryGallery(models.Model):
    """Model for ministry photo galleries."""

    ministry = models.ForeignKey(
        Ministry,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(
        upload_to='ministries/gallery/',
        help_text="Recommended size: 800x600 pixels"
    )
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ministry Gallery Image"
        verbose_name_plural = "Ministry Gallery Images"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.ministry.name} - Image {self.id}"
