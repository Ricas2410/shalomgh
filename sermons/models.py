"""
Models for sermon management and archive.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import URLValidator
from pages.models import LeadershipProfile


class Speaker(models.Model):
    """Model for sermon speakers."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='speakers/',
        blank=True,
        help_text="Recommended size: 300x300 pixels"
    )

    # Link to leadership profile if applicable
    leadership_profile = models.OneToOneField(
        LeadershipProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='speaker_profile'
    )

    # Contact Information
    email = models.EmailField(blank=True)
    website = models.URLField(validators=[URLValidator()], blank=True)

    # Display Settings
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Speaker"
        verbose_name_plural = "Speakers"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sermons:speaker_detail', kwargs={'slug': self.slug})


class SermonSeries(models.Model):
    """Model for sermon series."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='sermon_series/',
        blank=True,
        help_text="Recommended size: 800x400 pixels"
    )

    # Date Information
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    # Display Settings
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sermon Series"
        verbose_name_plural = "Sermon Series"
        ordering = ['-start_date', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sermons:series_detail', kwargs={'slug': self.slug})

    def get_sermon_count(self):
        return self.sermons.filter(is_published=True).count()


class Sermon(models.Model):
    """Model for individual sermons."""

    MEDIA_TYPE_CHOICES = [
        ('video', 'Video'),
        ('audio', 'Audio Only'),
        ('both', 'Both Video and Audio'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    # Speaker and Series
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.CASCADE,
        related_name='sermons'
    )
    series = models.ForeignKey(
        SermonSeries,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='sermons'
    )

    # Date and Time
    date_preached = models.DateField()
    duration = models.DurationField(
        blank=True,
        null=True,
        help_text="Duration in HH:MM:SS format"
    )

    # Media Information
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='video'
    )

    # Video URLs (YouTube, Vimeo, etc.)
    video_url = models.URLField(
        validators=[URLValidator()],
        blank=True,
        help_text="YouTube, Vimeo, or other video platform URL"
    )

    # Audio File
    audio_file = models.FileField(
        upload_to='sermons/audio/',
        blank=True,
        help_text="Upload MP3 or other audio file"
    )

    # Transcript and Notes
    transcript = models.TextField(
        blank=True,
        help_text="Full transcript of the sermon"
    )
    notes = models.TextField(
        blank=True,
        help_text="Sermon notes or outline"
    )

    # Scripture References
    scripture_references = models.TextField(
        blank=True,
        help_text="Bible verses referenced in the sermon"
    )

    # Tags and Categories
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated tags"
    )

    # Thumbnail
    thumbnail = models.ImageField(
        upload_to='sermons/thumbnails/',
        blank=True,
        help_text="Recommended size: 800x450 pixels"
    )

    # Download Files
    pdf_notes = models.FileField(
        upload_to='sermons/pdf/',
        blank=True,
        help_text="PDF version of sermon notes"
    )

    # Statistics
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)

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
        verbose_name = "Sermon"
        verbose_name_plural = "Sermons"
        ordering = ['-date_preached', '-created_at']
        indexes = [
            models.Index(fields=['-date_preached']),
            models.Index(fields=['is_published']),
            models.Index(fields=['speaker']),
            models.Index(fields=['series']),
        ]

    def __str__(self):
        return f"{self.title} - {self.speaker.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.date_preached}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sermons:detail', kwargs={'pk': self.pk})

    def get_tags_list(self):
        """Return tags as a list."""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

    def increment_view_count(self):
        """Increment the view count."""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def increment_download_count(self):
        """Increment the download count."""
        self.download_count += 1
        self.save(update_fields=['download_count'])
