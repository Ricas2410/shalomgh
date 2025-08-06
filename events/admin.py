from django.contrib import admin
from .models import EventCategory, Event


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'color')
        }),
        ('Settings', {
            'fields': ('is_active',)
        })
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'start_time', 'event_type', 'category', 'is_published', 'is_featured']
    list_filter = ['is_published', 'is_featured', 'event_type', 'category', 'start_date', 'is_all_day', 'is_online']
    search_fields = ['title', 'description', 'location_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    raw_id_fields = ['category']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'short_description', 'featured_image')
        }),
        ('Category & Type', {
            'fields': ('category', 'event_type')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date', 'start_time', 'end_time', 'is_all_day')
        }),
        ('Recurrence', {
            'fields': ('recurrence', 'recurrence_end_date'),
            'classes': ('collapse',)
        }),
        ('Location', {
            'fields': ('location_name', 'address', 'is_online', 'online_link')
        }),
        ('Registration', {
            'fields': ('requires_registration', 'registration_url', 'max_attendees', 'registration_deadline'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_published', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
