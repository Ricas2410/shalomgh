"""
Management command to perform SEO audit and optimization checks.
"""
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.test import Client
from django.conf import settings
from core.models import SiteSetting
from sermons.models import Sermon
from events.models import Event
from ministries.models import Ministry
from urllib.parse import urljoin


class Command(BaseCommand):
    help = 'Perform SEO audit and optimization checks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-urls',
            action='store_true',
            help='Check URL accessibility and response codes',
        )
        parser.add_argument(
            '--check-meta',
            action='store_true',
            help='Check meta tags and SEO elements',
        )
        parser.add_argument(
            '--check-images',
            action='store_true',
            help='Check for missing images and alt tags',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Run all SEO checks',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting SEO Audit for Church Website')
        )
        self.stdout.write('=' * 50)

        if options['all'] or options['check_urls']:
            self.check_urls()

        if options['all'] or options['check_meta']:
            self.check_meta_tags()

        if options['all'] or options['check_images']:
            self.check_images()

        self.check_site_settings()
        self.check_sitemap()
        self.check_robots_txt()

        self.stdout.write(
            self.style.SUCCESS('\nSEO Audit Complete!')
        )

    def check_urls(self):
        """Check URL accessibility and response codes."""
        self.stdout.write('\n📊 Checking URL Accessibility...')
        
        client = Client()
        urls_to_check = [
            ('Home', reverse('core:home')),
            ('About', reverse('pages:about')),
            ('Sermons', reverse('sermons:list')),
            ('Events', reverse('events:list')),
            ('Ministries', reverse('ministries:list')),
            ('Contact', reverse('core:contact')),
            ('Giving', reverse('core:giving')),
        ]

        for name, url in urls_to_check:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    self.stdout.write(f'  ✅ {name}: {url} - OK')
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️  {name}: {url} - Status {response.status_code}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ {name}: {url} - Error: {str(e)}')
                )

    def check_meta_tags(self):
        """Check meta tags and SEO elements."""
        self.stdout.write('\n🏷️  Checking Meta Tags...')
        
        # Check sermons without meta descriptions
        sermons_without_meta = Sermon.objects.filter(
            is_published=True,
            meta_description__isnull=True
        ).count()
        
        if sermons_without_meta > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {sermons_without_meta} sermons missing meta descriptions')
            )
        else:
            self.stdout.write('  ✅ All published sermons have meta descriptions')

        # Check events without meta descriptions
        events_without_meta = Event.objects.filter(
            meta_description__isnull=True
        ).count()
        
        if events_without_meta > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {events_without_meta} events missing meta descriptions')
            )
        else:
            self.stdout.write('  ✅ All events have meta descriptions')

        # Check ministries without meta descriptions
        ministries_without_meta = Ministry.objects.filter(
            is_active=True,
            meta_description__isnull=True
        ).count()
        
        if ministries_without_meta > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {ministries_without_meta} ministries missing meta descriptions')
            )
        else:
            self.stdout.write('  ✅ All active ministries have meta descriptions')

    def check_images(self):
        """Check for missing images and optimization."""
        self.stdout.write('\n🖼️  Checking Images...')
        
        # Check for missing sermon thumbnails
        sermons_without_thumbnails = Sermon.objects.filter(
            is_published=True,
            thumbnail__isnull=True
        ).count()
        
        if sermons_without_thumbnails > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {sermons_without_thumbnails} sermons missing thumbnails')
            )
        else:
            self.stdout.write('  ✅ All published sermons have thumbnails')

        # Check for missing event images
        events_without_images = Event.objects.filter(
            featured_image__isnull=True
        ).count()
        
        if events_without_images > 0:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {events_without_images} events missing featured images')
            )
        else:
            self.stdout.write('  ✅ All events have featured images')

    def check_site_settings(self):
        """Check site settings for SEO completeness."""
        self.stdout.write('\n⚙️  Checking Site Settings...')
        
        try:
            settings_obj = SiteSetting.get_settings()
            
            if not settings_obj.meta_description:
                self.stdout.write(
                    self.style.WARNING('  ⚠️  Site meta description is missing')
                )
            else:
                self.stdout.write('  ✅ Site meta description is set')

            if not settings_obj.meta_keywords:
                self.stdout.write(
                    self.style.WARNING('  ⚠️  Site meta keywords are missing')
                )
            else:
                self.stdout.write('  ✅ Site meta keywords are set')

            # Check social media URLs
            social_urls = [
                ('Facebook', settings_obj.facebook_url),
                ('Twitter', settings_obj.twitter_url),
                ('Instagram', settings_obj.instagram_url),
                ('YouTube', settings_obj.youtube_url),
            ]
            
            for platform, url in social_urls:
                if url:
                    self.stdout.write(f'  ✅ {platform} URL is set')
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️  {platform} URL is missing')
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'  ❌ Error checking site settings: {str(e)}')
            )

    def check_sitemap(self):
        """Check sitemap accessibility."""
        self.stdout.write('\n🗺️  Checking Sitemap...')

        try:
            # Test sitemap generation directly
            from django.contrib.sitemaps.views import sitemap
            from django.http import HttpRequest
            from church_website.urls import sitemaps

            request = HttpRequest()
            request.method = 'GET'
            request.META['SERVER_NAME'] = 'localhost'
            request.META['SERVER_PORT'] = '8000'

            response = sitemap(request, sitemaps=sitemaps)

            if response.status_code == 200:
                self.stdout.write('  ✅ Sitemap generation works correctly')

                # Render the response to get content
                try:
                    response.render()
                    content = response.content.decode('utf-8')
                    if '<url>' in content:
                        url_count = content.count('<url>')
                        self.stdout.write(f'  ✅ Sitemap contains {url_count} URLs')
                    else:
                        self.stdout.write(
                            self.style.WARNING('  ⚠️  Sitemap appears to be empty')
                        )
                except Exception as render_error:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️  Could not check sitemap content: {str(render_error)}')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Sitemap generation failed - Status {response.status_code}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'  ❌ Error checking sitemap: {str(e)}')
            )

    def check_robots_txt(self):
        """Check robots.txt accessibility."""
        self.stdout.write('\n🤖 Checking Robots.txt...')

        try:
            # Test robots.txt template rendering
            from django.template.loader import render_to_string
            from django.http import HttpRequest

            request = HttpRequest()
            request.method = 'GET'
            request.META['SERVER_NAME'] = 'localhost'
            request.META['SERVER_PORT'] = '8000'
            request.META['wsgi.url_scheme'] = 'http'

            content = render_to_string('robots.txt', {'request': request})

            if content:
                self.stdout.write('  ✅ Robots.txt template renders correctly')

                if 'Sitemap:' in content:
                    self.stdout.write('  ✅ Robots.txt contains sitemap reference')
                else:
                    self.stdout.write(
                        self.style.WARNING('  ⚠️  Robots.txt missing sitemap reference')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR('  ❌ Robots.txt template is empty')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'  ❌ Error checking robots.txt: {str(e)}')
            )
