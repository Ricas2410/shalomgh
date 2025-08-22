"""
Views for live streaming management.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from urllib.parse import urlencode, urlparse, parse_qs
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from .models import LiveStream, StreamPlatform, StreamBroadcast, StreamAnalytics


class AdminRequiredMixin(LoginRequiredMixin):
    """Mixin to require admin/staff access."""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'You need admin privileges to access this page.')
            return redirect('custom_admin:login')
        return super().dispatch(request, *args, **kwargs)


class LiveStreamListView(AdminRequiredMixin, ListView):
    """List all live streams."""
    model = LiveStream
    template_name = 'custom_admin/livestream_list.html'
    context_object_name = 'streams'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = LiveStream.objects.select_related('created_by').prefetch_related('platforms')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by stream type
        stream_type = self.request.GET.get('stream_type')
        if stream_type:
            queryset = queryset.filter(stream_type=stream_type)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = LiveStream.STATUS_CHOICES
        context['stream_type_choices'] = LiveStream.STREAM_TYPE_CHOICES
        context['current_status'] = self.request.GET.get('status', '')
        context['current_stream_type'] = self.request.GET.get('stream_type', '')
        context['search'] = self.request.GET.get('search', '')
        
        # Get live streams count
        context['live_count'] = LiveStream.objects.filter(status='live').count()
        context['upcoming_count'] = LiveStream.objects.filter(
            status='scheduled',
            scheduled_start__gt=timezone.now()
        ).count()
        
        return context

    def _build_embed_url(self, platform_type: str, platform_url: str, host: str) -> str:
        """Return an embeddable player URL for supported platforms.
        Supports: youtube, vimeo, twitch, facebook. Falls back to the given URL.
        """
        if not platform_url:
            return ''
        url = platform_url
        p = urlparse(url)

        # YouTube: watch?v=VIDEO_ID or youtu.be/VIDEO_ID -> youtube.com/embed/VIDEO_ID
        if platform_type == 'youtube':
            video_id = ''
            if 'youtube.com' in p.netloc:
                qs = parse_qs(p.query)
                video_id = (qs.get('v') or [''])[0]
            elif 'youtu.be' in p.netloc:
                # path like /VIDEO_ID
                video_id = p.path.strip('/')
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}?" + urlencode({'autoplay': 0, 'rel': 0})
            # Already an embed or playlist
            if '/embed/' in p.path:
                return url
            return url

        # Vimeo: vimeo.com/ID -> player.vimeo.com/video/ID
        if platform_type == 'vimeo':
            if 'vimeo.com' in p.netloc:
                parts = [seg for seg in p.path.split('/') if seg]
                if parts and parts[0].isdigit():
                    return f"https://player.vimeo.com/video/{parts[0]}"
            return url

        # Twitch: channel or video embeds require parent param
        if platform_type == 'twitch':
            # Try to detect channel name from URL like twitch.tv/{channel}
            channel = ''
            if 'twitch.tv' in p.netloc:
                parts = [seg for seg in p.path.split('/') if seg]
                if parts:
                    # ignore paths like videos/12345 for simplicity
                    channel = parts[0]
            params = {'parent': host, 'autoplay': 'false'}
            if channel:
                base = 'https://player.twitch.tv/?' + urlencode({'channel': channel})
                return base + '&' + urlencode(params)
            return 'https://player.twitch.tv/?' + urlencode(params)

        # Facebook: use video plugin with the URL encoded
        if platform_type == 'facebook':
            return 'https://www.facebook.com/plugins/video.php?' + urlencode({'href': url, 'show_text': 'false', 'autoplay': 'false'})

        # Fallback to provided URL
        return url


class LiveStreamDetailView(AdminRequiredMixin, DetailView):
    """View live stream details."""
    model = LiveStream
    template_name = 'custom_admin/livestream_detail.html'
    context_object_name = 'stream'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        broadcasts = list(self.object.streambroadcast_set.select_related('platform'))
        # Annotate each broadcast with an embeddable URL
        host = self.request.get_host()
        for b in broadcasts:
            context_url = (b.platform_url or '').strip()
            b.embed_url = self._build_embed_url(b.platform.platform_type, context_url, host)
        context['broadcasts'] = broadcasts
        
        # Get analytics if available
        try:
            context['analytics'] = self.object.analytics
        except StreamAnalytics.DoesNotExist:
            context['analytics'] = None
        
        return context


class LiveStreamCreateView(AdminRequiredMixin, CreateView):
    """Create a new live stream."""
    model = LiveStream
    template_name = 'custom_admin/livestream_form.html'
    fields = [
        'title', 'description', 'stream_type', 'scheduled_start', 'scheduled_end',
        'obs_scene_collection', 'obs_profile', 'thumbnail', 'is_public',
        'enable_chat', 'enable_recording'
    ]
    success_url = reverse_lazy('custom_admin:livestream:list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Live stream "{form.instance.title}" created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schedule New Live Stream'
        context['platforms'] = StreamPlatform.objects.filter(is_active=True)
        return context


class LiveStreamUpdateView(AdminRequiredMixin, UpdateView):
    """Update an existing live stream."""
    model = LiveStream
    template_name = 'custom_admin/livestream_form.html'
    fields = [
        'title', 'description', 'stream_type', 'scheduled_start', 'scheduled_end',
        'obs_scene_collection', 'obs_profile', 'thumbnail', 'is_public',
        'enable_chat', 'enable_recording', 'status'
    ]
    success_url = reverse_lazy('custom_admin:livestream:list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Live stream "{form.instance.title}" updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Live Stream: {self.object.title}'
        context['platforms'] = StreamPlatform.objects.filter(is_active=True)
        context['broadcasts'] = self.object.streambroadcast_set.select_related('platform')
        return context


class LiveStreamDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a live stream."""
    model = LiveStream
    template_name = 'custom_admin/livestream_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:livestream:list')
    
    def delete(self, request, *args, **kwargs):
        stream = self.get_object()
        messages.success(request, f'Live stream "{stream.title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


class StreamPlatformListView(AdminRequiredMixin, ListView):
    """List all stream platforms."""
    model = StreamPlatform
    template_name = 'custom_admin/platform_list.html'
    context_object_name = 'platforms'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platform_choices'] = StreamPlatform.PLATFORM_CHOICES
        return context


class StreamPlatformCreateView(AdminRequiredMixin, CreateView):
    """Create a new stream platform."""
    model = StreamPlatform
    template_name = 'custom_admin/platform_form.html'
    fields = ['name', 'platform_type', 'stream_key', 'rtmp_url', 'api_key', 'is_active']
    success_url = reverse_lazy('custom_admin:livestream:platform_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Platform "{form.instance.name}" created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Platform'
        return context


class StreamPlatformUpdateView(AdminRequiredMixin, UpdateView):
    """Update an existing stream platform."""
    model = StreamPlatform
    template_name = 'custom_admin/platform_form.html'
    fields = ['name', 'platform_type', 'stream_key', 'rtmp_url', 'api_key', 'is_active']
    success_url = reverse_lazy('custom_admin:livestream:platform_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Platform "{form.instance.name}" updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Platform: {self.object.name}'
        return context


class StreamPlatformDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a stream platform."""
    model = StreamPlatform
    template_name = 'custom_admin/platform_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:livestream:platform_list')
    
    def delete(self, request, *args, **kwargs):
        platform = self.get_object()
        messages.success(request, f'Platform "{platform.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


# API Views for real-time updates
def stream_status_api(request, stream_id):
    """API endpoint to get stream status."""
    try:
        stream = LiveStream.objects.get(id=stream_id)
        data = {
            'status': stream.status,
            'viewer_count': stream.viewer_count,
            'is_live': stream.is_live,
            'actual_start': stream.actual_start.isoformat() if stream.actual_start else None,
        }
        return JsonResponse(data)
    except LiveStream.DoesNotExist:
        return JsonResponse({'error': 'Stream not found'}, status=404)


def update_stream_status(request, stream_id):
    """API endpoint to update stream status."""
    if request.method == 'POST':
        try:
            stream = LiveStream.objects.get(id=stream_id)
            new_status = request.POST.get('status')
            
            if new_status in dict(LiveStream.STATUS_CHOICES):
                old_status = stream.status
                stream.status = new_status
                
                # Update timestamps based on status change
                if new_status == 'live' and old_status != 'live':
                    stream.actual_start = timezone.now()
                elif new_status == 'ended' and old_status == 'live':
                    stream.actual_end = timezone.now()
                
                stream.save()
                
                return JsonResponse({
                    'success': True,
                    'status': stream.status,
                    'message': f'Stream status updated to {stream.get_status_display()}'
                })
            else:
                return JsonResponse({'error': 'Invalid status'}, status=400)
                
        except LiveStream.DoesNotExist:
            return JsonResponse({'error': 'Stream not found'}, status=404)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Dashboard view for live streaming overview
class LiveStreamDashboardView(AdminRequiredMixin, ListView):
    """Dashboard view for live streaming overview."""
    model = LiveStream
    template_name = 'custom_admin/livestream_dashboard.html'
    context_object_name = 'recent_streams'
    
    def get_queryset(self):
        return LiveStream.objects.select_related('created_by').order_by('-created_at')[:10]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Current live streams
        context['live_streams'] = LiveStream.objects.filter(status='live').select_related('created_by')
        
        # Upcoming streams (next 7 days)
        context['upcoming_streams'] = LiveStream.objects.filter(
            status='scheduled',
            scheduled_start__gte=timezone.now(),
            scheduled_start__lte=timezone.now() + timezone.timedelta(days=7)
        ).order_by('scheduled_start')[:5]
        
        # Statistics
        context['stats'] = {
            'total_streams': LiveStream.objects.count(),
            'live_count': LiveStream.objects.filter(status='live').count(),
            'scheduled_count': LiveStream.objects.filter(status='scheduled').count(),
            'total_platforms': StreamPlatform.objects.filter(is_active=True).count(),
        }
        
        # Recent analytics
        recent_streams_with_analytics = LiveStream.objects.filter(
            analytics__isnull=False,
            status='ended'
        ).select_related('analytics').order_by('-actual_end')[:5]
        
        context['recent_analytics'] = recent_streams_with_analytics
        
        return context
