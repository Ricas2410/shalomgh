from django.contrib import admin
from .models import Ministry, MinistryGallery


class MinistryGalleryInline(admin.TabularInline):
    """Inline admin for ministry gallery images."""
    model = MinistryGallery
    extra = 1
    fields = ['image', 'caption', 'display_order']
    ordering = ['display_order']


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    """Admin configuration for Ministry model."""
    list_display = ['name', 'ministry_type', 'leader', 'is_active', 'is_featured', 'display_order']
    list_filter = ['ministry_type', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'short_description', 'description']
    list_editable = ['is_active', 'is_featured', 'display_order']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['assistant_leaders']
    inlines = [MinistryGalleryInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'ministry_type', 'short_description', 'description')
        }),
        ('Mission & Activities', {
            'fields': ('mission_statement', 'activities', 'requirements')
        }),
        ('Leadership', {
            'fields': ('leader', 'assistant_leaders')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Meeting Information', {
            'fields': ('meeting_day', 'meeting_time', 'meeting_location')
        }),
        ('Age Group', {
            'fields': ('min_age', 'max_age')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_featured', 'display_order')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('leader').prefetch_related('assistant_leaders')


@admin.register(MinistryGallery)
class MinistryGalleryAdmin(admin.ModelAdmin):
    """Admin configuration for MinistryGallery model."""
    list_display = ['ministry', 'caption', 'display_order', 'created_at']
    list_filter = ['ministry', 'created_at']
    search_fields = ['ministry__name', 'caption']
    list_editable = ['display_order']
    ordering = ['ministry', 'display_order', '-created_at']

    fieldsets = (
        ('Gallery Image', {
            'fields': ('ministry', 'image', 'caption')
        }),
        ('Display Settings', {
            'fields': ('display_order',)
        }),
    )
