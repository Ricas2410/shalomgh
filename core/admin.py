from django.contrib import admin
from .models import SiteSetting, ContactMessage, PageImage, ServiceTime, KeyMilestone


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'church_name', 'updated_at']
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'church_name', 'tagline', 'welcome_message')
        }),
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'service_times')
        }),
        ('External URLs', {
            'fields': ('member_portal_url', 'giving_platform_url')
        }),
        ('Payment Configuration', {
            'fields': ('enable_paystack', 'paystack_public_key', 'paystack_secret_key')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Google Services', {
            'fields': ('google_maps_api_key', 'google_analytics_id')
        }),
        ('Location & Directions', {
            'fields': (
                'map_query', 'map_embed_url',
                'directions_heading', 'directions_details',
                'directions_link_text', 'directions_link_url'
            ),
            'description': 'Configure map and directions content for the Location page'
        }),
        ('CTA Section Media', {
            'fields': ('cta_image', 'cta_youtube_url'),
            'description': 'Optional media content for Call-to-Action sections'
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['mark_as_read', 'mark_as_replied']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_replied(self, request, queryset):
        queryset.update(is_replied=True)
    mark_as_replied.short_description = "Mark selected messages as replied"


@admin.register(PageImage)
class PageImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_section', 'display_order', 'is_active', 'created_at']
    list_filter = ['page_section', 'is_active', 'created_at']
    search_fields = ['title', 'alt_text', 'caption']
    list_editable = ['display_order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Image Information', {
            'fields': ('page_section', 'title', 'image', 'fallback_url')
        }),
        ('Display Settings', {
            'fields': ('alt_text', 'caption', 'display_order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(ServiceTime)
class ServiceTimeAdmin(admin.ModelAdmin):
    """Admin configuration for ServiceTime model."""
    list_display = ['name', 'day', 'time', 'display_order', 'is_active']
    list_filter = ['day', 'is_active']
    search_fields = ['name', 'time']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'day']

    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'day', 'time')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )


@admin.register(KeyMilestone)
class KeyMilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'display_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['display_order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Milestone Information', {
            'fields': ('title', 'value', 'description', 'icon_class')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
