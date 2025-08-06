"""
Models for event management and calendar.
"""
from django.db import models
from django.urls import reverse
from django.core.validators import URLValidator
from django.utils import timezone


class EventCategory(models.Model):
    """Model for event categories."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=7,
        default='#0EC6EB',
        help_text="Hex color code for calendar display"
    )

    # Display Settings
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    """Model for church events."""

    EVENT_TYPE_CHOICES = [
        ('service', 'Church Service'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('social', 'Social Event'),
        ('outreach', 'Outreach'),
        ('meeting', 'Meeting'),
        ('special', 'Special Event'),
        ('other', 'Other'),
    ]

    RECURRENCE_CHOICES = [
        ('none', 'No Recurrence'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Brief description for calendar view"
    )

    # Category and Type
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='events'
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='other'
    )

    # Date and Time
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_all_day = models.BooleanField(default=False)

    # Recurrence
    recurrence = models.CharField(
        max_length=10,
        choices=RECURRENCE_CHOICES,
        default='none'
    )
    recurrence_end_date = models.DateField(
        blank=True,
        null=True,
        help_text="When to stop recurring events"
    )

    # Location
    location_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(
        validators=[URLValidator()],
        blank=True,
        help_text="Link for online events"
    )

    # Registration
    requires_registration = models.BooleanField(default=False)
    registration_url = models.URLField(
        validators=[URLValidator()],
        blank=True,
        help_text="External registration link"
    )
    max_attendees = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Maximum number of attendees (leave blank for unlimited)"
    )
    registration_deadline = models.DateTimeField(blank=True, null=True)

    # Media
    featured_image = models.ImageField(
        upload_to='events/',
        blank=True,
        help_text="Recommended size: 800x400 pixels"
    )

    # Contact Information
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    # Display Settings
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

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
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['start_date', 'start_time']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['is_published']),
            models.Index(fields=['category']),
            models.Index(fields=['event_type']),
        ]

    def __str__(self):
        return f"{self.title} - {self.start_date}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(f"{self.title}-{self.start_date}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    @property
    def is_past(self):
        """Check if the event is in the past."""
        if self.end_date:
            return self.end_date < timezone.now().date()
        return self.start_date < timezone.now().date()

    @property
    def is_today(self):
        """Check if the event is today."""
        today = timezone.now().date()
        if self.end_date:
            return self.start_date <= today <= self.end_date
        return self.start_date == today

    @property
    def is_upcoming(self):
        """Check if the event is upcoming."""
        return self.start_date > timezone.now().date()

    def get_duration_display(self):
        """Get formatted duration display."""
        if self.is_all_day:
            if self.end_date and self.end_date != self.start_date:
                return f"{self.start_date} - {self.end_date} (All Day)"
            return f"{self.start_date} (All Day)"

        if self.start_time and self.end_time:
            return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
        elif self.start_time:
            return self.start_time.strftime('%I:%M %p')

        return "Time TBD"
