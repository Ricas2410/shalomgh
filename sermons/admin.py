from django.contrib import admin
from .models import Speaker, SermonSeries, Sermon


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'bio', 'photo')
        }),
        ('Contact Information', {
            'fields': ('email', 'website', 'leadership_profile')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(SermonSeries)
class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_featured', 'is_active', 'get_sermon_count']
    list_filter = ['is_featured', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'get_sermon_count']
    date_hierarchy = 'start_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        ('Date Information', {
            'fields': ('start_date', 'end_date')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Statistics', {
            'fields': ('get_sermon_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'series', 'date_preached', 'media_type', 'is_published', 'is_featured', 'view_count']
    list_filter = ['is_published', 'is_featured', 'media_type', 'speaker', 'series', 'date_preached']
    search_fields = ['title', 'description', 'tags', 'scripture_references']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'view_count', 'download_count']
    date_hierarchy = 'date_preached'
    filter_horizontal = []
    raw_id_fields = ['speaker', 'series']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'thumbnail')
        }),
        ('Speaker & Series', {
            'fields': ('speaker', 'series')
        }),
        ('Date & Duration', {
            'fields': ('date_preached', 'duration')
        }),
        ('Media', {
            'fields': ('media_type', 'video_url', 'audio_file')
        }),
        ('Content', {
            'fields': ('transcript', 'notes', 'scripture_references', 'pdf_notes')
        }),
        ('Categorization', {
            'fields': ('tags',)
        }),
        ('Settings', {
            'fields': ('is_published', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'download_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
