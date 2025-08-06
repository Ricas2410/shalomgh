"""
Admin configuration for livestream app.
"""
from django.contrib import admin
from .models import StreamPlatform, LiveStream, StreamBroadcast, StreamChat, StreamAnalytics


@admin.register(StreamPlatform)
class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform_type', 'is_active', 'created_at']
    list_filter = ['platform_type', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'platform_type', 'is_active')
        }),
        ('Configuration', {
            'fields': ('stream_key', 'rtmp_url', 'api_key'),
            'description': 'Platform-specific configuration settings'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class StreamBroadcastInline(admin.TabularInline):
    model = StreamBroadcast
    extra = 1
    readonly_fields = ['broadcast_started', 'broadcast_ended', 'viewer_count', 'created_at']


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ['title', 'stream_type', 'status', 'scheduled_start', 'viewer_count', 'created_by']
    list_filter = ['status', 'stream_type', 'is_public', 'scheduled_start', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['actual_start', 'actual_end', 'viewer_count', 'created_at', 'updated_at']
    inlines = [StreamBroadcastInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'stream_type', 'thumbnail')
        }),
        ('Scheduling', {
            'fields': ('scheduled_start', 'scheduled_end', 'actual_start', 'actual_end')
        }),
        ('OBS Integration', {
            'fields': ('obs_scene_collection', 'obs_profile'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_public', 'enable_chat', 'enable_recording')
        }),
        ('Status', {
            'fields': ('status', 'viewer_count')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(StreamBroadcast)
class StreamBroadcastAdmin(admin.ModelAdmin):
    list_display = ['stream', 'platform', 'is_active', 'viewer_count', 'broadcast_started']
    list_filter = ['platform', 'is_active', 'broadcast_started']
    search_fields = ['stream__title', 'platform__name']
    readonly_fields = ['viewer_count', 'created_at', 'updated_at']


@admin.register(StreamChat)
class StreamChatAdmin(admin.ModelAdmin):
    list_display = ['stream', 'username', 'message_preview', 'platform', 'is_moderator', 'timestamp']
    list_filter = ['platform', 'is_moderator', 'is_hidden', 'timestamp']
    search_fields = ['username', 'message', 'stream__title']
    readonly_fields = ['timestamp']
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Message"


@admin.register(StreamAnalytics)
class StreamAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['stream', 'peak_viewers', 'total_views', 'total_chat_messages', 'stream_quality']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Stream', {
            'fields': ('stream',)
        }),
        ('Viewer Metrics', {
            'fields': ('peak_viewers', 'total_views', 'average_watch_time')
        }),
        ('Engagement Metrics', {
            'fields': ('total_chat_messages', 'likes_count', 'shares_count')
        }),
        ('Technical Metrics', {
            'fields': ('stream_quality', 'dropped_frames', 'bitrate_average')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
