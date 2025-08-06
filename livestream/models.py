"""
Models for live streaming management.
"""
from django.db import models
from django.urls import reverse
from django.core.validators import URLValidator
from django.utils import timezone
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    """Model for streaming platforms configuration."""
    
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube Live'),
        ('facebook', 'Facebook Live'),
        ('twitch', 'Twitch'),
        ('vimeo', 'Vimeo Live'),
        ('direct', 'Direct RTMP'),
        ('custom', 'Custom Platform'),
    ]
    
    name = models.CharField(max_length=100)
    platform_type = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    stream_key = models.CharField(
        max_length=500, 
        blank=True,
        help_text="Stream key for the platform"
    )
    rtmp_url = models.URLField(
        blank=True,
        help_text="RTMP server URL for streaming"
    )
    api_key = models.CharField(
        max_length=500, 
        blank=True,
        help_text="API key for platform integration"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Stream Platform"
        verbose_name_plural = "Stream Platforms"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_platform_type_display()})"


class LiveStream(models.Model):
    """Model for managing live streams."""
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live Now'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]
    
    STREAM_TYPE_CHOICES = [
        ('service', 'Church Service'),
        ('prayer', 'Prayer Meeting'),
        ('bible_study', 'Bible Study'),
        ('conference', 'Conference'),
        ('special_event', 'Special Event'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    stream_type = models.CharField(
        max_length=20, 
        choices=STREAM_TYPE_CHOICES,
        default='service'
    )
    
    # Scheduling
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField(blank=True, null=True)
    actual_start = models.DateTimeField(blank=True, null=True)
    actual_end = models.DateTimeField(blank=True, null=True)
    
    # Stream Configuration
    platforms = models.ManyToManyField(
        StreamPlatform,
        through='StreamBroadcast',
        related_name='streams'
    )
    
    # OBS Integration
    obs_scene_collection = models.CharField(
        max_length=200, 
        blank=True,
        help_text="OBS Scene Collection name"
    )
    obs_profile = models.CharField(
        max_length=200, 
        blank=True,
        help_text="OBS Profile name"
    )
    
    # Stream Settings
    thumbnail = models.ImageField(
        upload_to='livestream/thumbnails/',
        blank=True,
        help_text="Stream thumbnail/preview image"
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Make stream publicly visible"
    )
    enable_chat = models.BooleanField(
        default=True,
        help_text="Enable chat for the stream"
    )
    enable_recording = models.BooleanField(
        default=True,
        help_text="Record the stream"
    )
    
    # Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    viewer_count = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='created_streams'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Live Stream"
        verbose_name_plural = "Live Streams"
        ordering = ['-scheduled_start']
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_start.strftime('%Y-%m-%d %H:%M')}"
    
    def get_absolute_url(self):
        return reverse('livestream:detail', kwargs={'pk': self.pk})
    
    @property
    def is_live(self):
        """Check if stream is currently live."""
        return self.status == 'live'
    
    @property
    def is_upcoming(self):
        """Check if stream is upcoming."""
        return self.status == 'scheduled' and self.scheduled_start > timezone.now()
    
    @property
    def duration(self):
        """Get stream duration if ended."""
        if self.actual_start and self.actual_end:
            return self.actual_end - self.actual_start
        return None


class StreamBroadcast(models.Model):
    """Through model for stream-platform relationship."""
    
    stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE)
    
    # Platform-specific settings
    platform_stream_id = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Stream ID from the platform"
    )
    platform_url = models.URLField(
        blank=True,
        help_text="Direct URL to the stream on platform"
    )
    custom_title = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Platform-specific title override"
    )
    custom_description = models.TextField(
        blank=True,
        help_text="Platform-specific description override"
    )
    
    # Status tracking
    is_active = models.BooleanField(default=True)
    broadcast_started = models.DateTimeField(blank=True, null=True)
    broadcast_ended = models.DateTimeField(blank=True, null=True)
    viewer_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Stream Broadcast"
        verbose_name_plural = "Stream Broadcasts"
        unique_together = ['stream', 'platform']
    
    def __str__(self):
        return f"{self.stream.title} on {self.platform.name}"


class StreamChat(models.Model):
    """Model for stream chat messages."""
    
    stream = models.ForeignKey(
        LiveStream, 
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    username = models.CharField(max_length=100)
    message = models.TextField()
    platform = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Platform where message originated"
    )
    is_moderator = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Stream Chat Message"
        verbose_name_plural = "Stream Chat Messages"
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.username}: {self.message[:50]}..."


class StreamAnalytics(models.Model):
    """Model for stream analytics and metrics."""
    
    stream = models.OneToOneField(
        LiveStream,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Viewer metrics
    peak_viewers = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    average_watch_time = models.DurationField(blank=True, null=True)
    
    # Engagement metrics
    total_chat_messages = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    
    # Technical metrics
    stream_quality = models.CharField(
        max_length=20,
        blank=True,
        help_text="Stream quality (1080p, 720p, etc.)"
    )
    dropped_frames = models.PositiveIntegerField(default=0)
    bitrate_average = models.PositiveIntegerField(
        default=0,
        help_text="Average bitrate in kbps"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Stream Analytics"
        verbose_name_plural = "Stream Analytics"
    
    def __str__(self):
        return f"Analytics for {self.stream.title}"
