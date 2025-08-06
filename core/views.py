"""
Core views for the church website.
"""
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import SiteSetting, ContactMessage, KeyMilestone
from .forms import ContactForm
from sermons.models import Sermon
from events.models import Event
from pages.models import LeadershipProfile


class HomeView(TemplateView):
    """Home page view."""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get site settings
        site_settings = SiteSetting.get_settings()

        # Get featured sermons (max 3 for homepage)
        featured_sermons = Sermon.objects.filter(
            is_published=True,
            is_featured=True
        ).select_related('speaker', 'series')[:3]

        # Get featured events (max 3 for homepage)
        featured_events = Event.objects.filter(
            is_published=True,
            is_featured=True,
            start_date__gte=timezone.now().date()
        ).order_by('start_date', 'start_time')[:3]

        # Get featured leadership (those marked to show on homepage)
        featured_leadership = LeadershipProfile.objects.filter(
            is_active=True,
            show_on_homepage=True
        ).order_by('display_order')[:4]

        context.update({
            'site_settings': site_settings,
            'featured_sermons': featured_sermons,
            'featured_events': featured_events,
            'featured_leadership': featured_leadership,
        })

        return context


class ContactView(FormView):
    """Contact page view."""
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSetting.get_settings()
        context['key_milestones'] = KeyMilestone.objects.filter(is_active=True).order_by('display_order', 'title')
        return context

    def form_valid(self, form):
        # Save the contact message
        contact_message = ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message'],
            phone=form.cleaned_data.get('phone', ''),
        )

        # Send email notification to admin
        try:
            send_mail(
                subject=f'New Contact Form Submission: {contact_message.subject}',
                message=f"""
                New contact form submission from {contact_message.name}

                Email: {contact_message.email}
                Phone: {contact_message.phone}
                Subject: {contact_message.subject}

                Message:
                {contact_message.message}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass  # Fail silently if email sending fails

        messages.success(
            self.request,
            'Thank you for your message! We will get back to you soon.'
        )
        return super().form_valid(form)


class GivingView(TemplateView):
    """Giving page view."""
    template_name = 'core/giving.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSetting.get_settings()
        return context


class PlanVisitView(TemplateView):
    """Plan your visit page view."""
    template_name = 'core/plan_visit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSetting.get_settings()
        return context
