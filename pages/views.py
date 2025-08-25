"""
Views for static pages and leadership information.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.db.models import Q
from urllib.parse import urlencode, urlparse, parse_qs

from .models import LeadershipProfile, PageContent, WelcomeSection
from core.models import SiteSetting
from livestream.models import LiveStream


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

        # Get General Overseer (if available)
        general_overseer = LeadershipProfile.objects.filter(
            is_active=True,
            position='general_overseer'
        ).order_by('display_order').first()

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
            'general_overseer': general_overseer,
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

        # Helper: build embeddable player URL for supported platforms
        def _build_embed_url(platform_type: str, platform_url: str, host: str) -> str:
            if not platform_url:
                return ''
            p = urlparse(platform_url)

            # YouTube
            if platform_type == 'youtube':
                video_id = ''
                if 'youtube.com' in p.netloc:
                    qs = parse_qs(p.query)
                    video_id = (qs.get('v') or [''])[0]
                elif 'youtu.be' in p.netloc:
                    video_id = p.path.strip('/')
                if video_id:
                    return f"https://www.youtube.com/embed/{video_id}?" + urlencode({'autoplay': 0, 'rel': 0})
                if '/embed/' in p.path:
                    return platform_url
                return platform_url

            # Vimeo
            if platform_type == 'vimeo':
                if 'vimeo.com' in p.netloc:
                    parts = [seg for seg in p.path.split('/') if seg]
                    if parts and parts[0].isdigit():
                        return f"https://player.vimeo.com/video/{parts[0]}"
                return platform_url

            # Twitch
            if platform_type == 'twitch':
                channel = ''
                if 'twitch.tv' in p.netloc:
                    parts = [seg for seg in p.path.split('/') if seg]
                    if parts:
                        channel = parts[0]
                params = {'parent': host, 'autoplay': 'false'}
                if channel:
                    base = 'https://player.twitch.tv/?' + urlencode({'channel': channel})
                    return base + '&' + urlencode(params)
                return 'https://player.twitch.tv/?' + urlencode(params)

            # Facebook
            if platform_type == 'facebook':
                return 'https://www.facebook.com/plugins/video.php?' + urlencode({'href': platform_url, 'show_text': 'false', 'autoplay': 'false'})

            # Fallback
            return platform_url

        # Determine the current or next available public stream
        stream = (
            LiveStream.objects.filter(is_public=True, status='live').order_by('-scheduled_start').first()
            or LiveStream.objects.filter(is_public=True).order_by('-scheduled_start').first()
        )

        embed_url = ''
        if stream:
            b = stream.streambroadcast_set.select_related('platform').order_by('-broadcast_started').first()
            if b and b.platform:
                embed_url = _build_embed_url(b.platform.platform_type, (b.platform_url or '').strip(), self.request.get_host())

        context.update({
            'site_settings': site_settings,
            'embed_url': embed_url,
        })

        return context
