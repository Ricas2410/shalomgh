"""
Management command to populate sample page images with fallback URLs.
"""
from django.core.management.base import BaseCommand
from core.models import PageImage


class Command(BaseCommand):
    help = 'Populate sample page images with fallback URLs'

    def handle(self, *args, **options):
        # Sample page images with fallback URLs from Unsplash
        sample_images = [
            {
                'page_section': 'home_hero',
                'title': 'Church Sanctuary Hero Image',
                'fallback_url': 'https://images.unsplash.com/photo-1507692049790-de58290a4334?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'Beautiful church sanctuary with wooden pews and stained glass windows',
                'caption': 'Welcome to our church family',
                'display_order': 0,
            },
            {
                'page_section': 'home_welcome',
                'title': 'Church Community Welcome Image',
                'fallback_url': 'https://images.unsplash.com/photo-1438032005730-c779502df39b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'alt_text': 'Diverse group of people in church fellowship',
                'caption': 'Join our welcoming community',
                'display_order': 0,
            },
            {
                'page_section': 'about_hero',
                'title': 'About Us Hero Background',
                'fallback_url': 'https://images.unsplash.com/photo-1519491050282-cf00c82424b4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'Church building exterior with cross',
                'caption': 'Our story and mission',
                'display_order': 0,
            },
            {
                'page_section': 'sermons_hero',
                'title': 'Sermons Page Hero Background',
                'fallback_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'Open Bible on pulpit with soft lighting',
                'caption': 'God\'s Word for today',
                'display_order': 0,
            },
            {
                'page_section': 'events_hero',
                'title': 'Events Page Hero Background',
                'fallback_url': 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'Church event with people gathering',
                'caption': 'Join us for upcoming events',
                'display_order': 0,
            },
            {
                'page_section': 'ministries_hero',
                'title': 'Ministries Page Hero Background',
                'fallback_url': 'https://images.unsplash.com/photo-1529390079861-591de354faf5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'People serving in ministry together',
                'caption': 'Serving God and community',
                'display_order': 0,
            },
            {
                'page_section': 'contact_hero',
                'title': 'Contact Page Hero Background',
                'fallback_url': 'https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'Church doors open welcoming visitors',
                'caption': 'We\'d love to hear from you',
                'display_order': 0,
            },
            {
                'page_section': 'giving_hero',
                'title': 'Giving Page Hero Background',
                'fallback_url': 'https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'Hands in prayer and giving',
                'caption': 'Generous hearts, faithful giving',
                'display_order': 0,
            },
            {
                'page_section': 'leadership_hero',
                'title': 'Leadership Page Hero Background',
                'fallback_url': 'https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'Church leadership team in discussion',
                'caption': 'Faithful shepherds serving God\'s people',
                'display_order': 0,
            },
            {
                'page_section': 'location_hero',
                'title': 'Location Page Hero Background',
                'fallback_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
                'alt_text': 'Church building with beautiful architecture',
                'caption': 'Visit us and feel at home',
                'display_order': 0,
            },
            {
                'page_section': 'worship_service',
                'title': 'Worship Service Photo',
                'fallback_url': 'https://images.unsplash.com/photo-1507692049790-de58290a4334?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'alt_text': 'Congregation in worship service',
                'caption': 'Sabbath Worship service',
                'display_order': 0,
            },
            {
                'page_section': 'youth_ministry',
                'title': 'Youth Ministry Photo',
                'fallback_url': 'https://images.unsplash.com/photo-1529390079861-591de354faf5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'alt_text': 'Young people in ministry activities',
                'caption': 'Youth ministry activities',
                'display_order': 0,
            },
        ]

        created_count = 0
        updated_count = 0

        for image_data in sample_images:
            page_image, created = PageImage.objects.get_or_create(
                page_section=image_data['page_section'],
                display_order=image_data['display_order'],
                defaults=image_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {page_image.title}')
                )
            else:
                # Update existing image with new data
                for key, value in image_data.items():
                    if key not in ['page_section', 'display_order']:
                        setattr(page_image, key, value)
                page_image.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated: {page_image.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created {created_count} new images, updated {updated_count} existing images.'
            )
        )
