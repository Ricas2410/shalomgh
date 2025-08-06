from django.contrib import admin
from .models import LeadershipProfile, PageContent, WelcomeSection


@admin.register(LeadershipProfile)
class LeadershipProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'email', 'is_active', 'display_order']
    list_filter = ['position', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'last_name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'position', 'custom_position')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Profile', {
            'fields': ('photo', 'bio')
        }),
        ('Ministry Information', {
            'fields': ('years_in_ministry', 'specializations', 'education')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order')
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'is_published', 'updated_at']
    list_filter = ['page', 'is_published']
    search_fields = ['title', 'content']
    list_editable = ['is_published']

    fieldsets = (
        ('Page Information', {
            'fields': ('page', 'title')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('SEO', {
            'fields': ('meta_description',)
        }),
        ('Display Settings', {
            'fields': ('is_published',)
        }),
    )


@admin.register(WelcomeSection)
class WelcomeSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'content']
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'content')
        }),
        ('Image', {
            'fields': ('image', 'image_alt_text')
        }),
        ('Features', {
            'fields': (
                'feature_1_title', 'feature_1_description',
                'feature_2_title', 'feature_2_description',
                'feature_3_title', 'feature_3_description'
            )
        }),
        ('Display Settings', {
            'fields': ('is_active',)
        }),
    )
