"""
Management command to generate comprehensive SEO sitemap.
"""
from django.core.management.base import BaseCommand
from django.contrib.sitemaps import ping_google
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import xml.etree.ElementTree as ET
import os


class Command(BaseCommand):
    help = 'Generate comprehensive SEO sitemap for the church website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ping-google',
            action='store_true',
            help='Ping Google after generating sitemap',
        )

    def handle(self, *args, **options):
        self.stdout.write('Generating comprehensive SEO sitemap...')
        
        # Create sitemap XML
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
        
        # Static pages with high priority
        static_pages = [
            {'url': '/', 'priority': '1.0', 'changefreq': 'daily'},
            {'url': '/about/', 'priority': '0.9', 'changefreq': 'weekly'},
            {'url': '/sermons/', 'priority': '0.9', 'changefreq': 'daily'},
            {'url': '/events/', 'priority': '0.8', 'changefreq': 'daily'},
            {'url': '/ministries/', 'priority': '0.8', 'changefreq': 'weekly'},
            {'url': '/giving/', 'priority': '0.7', 'changefreq': 'monthly'},
            {'url': '/contact/', 'priority': '0.7', 'changefreq': 'monthly'},
            {'url': '/plan-visit/', 'priority': '0.8', 'changefreq': 'monthly'},
            {'url': '/livestream/', 'priority': '0.9', 'changefreq': 'daily'},
        ]
        
        for page in static_pages:
            url_elem = ET.SubElement(urlset, 'url')
            ET.SubElement(url_elem, 'loc').text = f"https://shalomgh.com{page['url']}"
            ET.SubElement(url_elem, 'lastmod').text = timezone.now().strftime('%Y-%m-%d')
            ET.SubElement(url_elem, 'changefreq').text = page['changefreq']
            ET.SubElement(url_elem, 'priority').text = page['priority']
        
        # Add dynamic content (sermons, events, etc.)
        try:
            from sermons.models import Sermon
            for sermon in Sermon.objects.filter(is_published=True)[:100]:  # Limit for performance
                url_elem = ET.SubElement(urlset, 'url')
                ET.SubElement(url_elem, 'loc').text = f"https://shalomgh.com/sermons/{sermon.slug}/"
                ET.SubElement(url_elem, 'lastmod').text = sermon.updated_at.strftime('%Y-%m-%d')
                ET.SubElement(url_elem, 'changefreq').text = 'monthly'
                ET.SubElement(url_elem, 'priority').text = '0.7'
                
                # Add image if available
                if sermon.thumbnail:
                    image_elem = ET.SubElement(url_elem, 'image:image')
                    ET.SubElement(image_elem, 'image:loc').text = f"https://shalomgh.com{sermon.thumbnail.url}"
                    ET.SubElement(image_elem, 'image:title').text = sermon.title
        except ImportError:
            pass
        
        try:
            from events.models import Event
            for event in Event.objects.filter(is_published=True)[:50]:
                url_elem = ET.SubElement(urlset, 'url')
                ET.SubElement(url_elem, 'loc').text = f"https://shalomgh.com/events/{event.slug}/"
                ET.SubElement(url_elem, 'lastmod').text = event.updated_at.strftime('%Y-%m-%d')
                ET.SubElement(url_elem, 'changefreq').text = 'weekly'
                ET.SubElement(url_elem, 'priority').text = '0.6'
        except ImportError:
            pass
        
        # Write sitemap to file
        tree = ET.ElementTree(urlset)
        sitemap_path = os.path.join(settings.STATIC_ROOT or 'static', 'sitemap.xml')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(sitemap_path), exist_ok=True)
        
        tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated sitemap at {sitemap_path}')
        )
        
        # Ping Google if requested
        if options['ping_google']:
            try:
                ping_google('/sitemap.xml')
                self.stdout.write(
                    self.style.SUCCESS('Successfully pinged Google about sitemap update')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to ping Google: {e}')
                )
