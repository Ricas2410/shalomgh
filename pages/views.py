"""
Views for static pages and leadership information.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.db.models import Q

from .models import LeadershipProfile, PageContent, WelcomeSection
from core.models import SiteSetting


class AboutView(TemplateView):
    """About Us main page view."""
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get about page content
        about_content = PageContent.objects.filter(
            page='about',
            is_published=True
        ).first()

        # Get featured leadership (first 4)
        featured_leadership = LeadershipProfile.objects.filter(
            is_active=True
        ).order_by('display_order')[:4]

        # Get welcome section
        welcome_section = WelcomeSection.get_active_welcome()

        context.update({
            'site_settings': site_settings,
            'about_content': about_content,
            'featured_leadership': featured_leadership,
            'welcome_section': welcome_section,
        })

        return context


class OurStoryView(TemplateView):
    """Our Story page view."""
    template_name = 'pages/our_story.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get our story content
        story_content = PageContent.objects.filter(
            page='our_story',
            is_published=True
        ).first()

        context.update({
            'site_settings': site_settings,
            'story_content': story_content,
        })

        return context


class BeliefsView(TemplateView):
    """Our Beliefs page view."""
    template_name = 'pages/beliefs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get beliefs content
        beliefs_content = PageContent.objects.filter(
            page='beliefs',
            is_published=True
        ).first()

        context.update({
            'site_settings': site_settings,
            'beliefs_content': beliefs_content,
        })

        return context


class LeadershipView(TemplateView):
    """Leadership team page view."""
    template_name = 'pages/leadership.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get all active leadership profiles
        leadership_profiles = LeadershipProfile.objects.filter(
            is_active=True
        ).order_by('display_order', 'last_name', 'first_name')

        # Group leadership by position for better organization
        leadership_by_position = {}
        for profile in leadership_profiles:
            position = profile.get_position_display()
            if position not in leadership_by_position:
                leadership_by_position[position] = []
            leadership_by_position[position].append(profile)

        context.update({
            'site_settings': site_settings,
            'leadership_profiles': leadership_profiles,
            'leadership_by_position': leadership_by_position,
        })

        return context


class LeadershipDetailView(DetailView):
    """Individual leadership profile detail view."""
    model = LeadershipProfile
    template_name = 'pages/leadership_detail.html'
    context_object_name = 'leader'

    def get_queryset(self):
        return LeadershipProfile.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get other leadership members (excluding current one)
        other_leaders = LeadershipProfile.objects.filter(
            is_active=True
        ).exclude(pk=self.object.pk).order_by('display_order')[:3]

        context.update({
            'site_settings': site_settings,
            'other_leaders': other_leaders,
        })

        return context


class LocationView(TemplateView):
    """Location and service times page view."""
    template_name = 'pages/location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        context.update({
            'site_settings': site_settings,
        })

        return context


class OnlineTVView(TemplateView):
    """Online TV streaming page view."""
    template_name = 'pages/online_tv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        context.update({
            'site_settings': site_settings,
        })

        return context
