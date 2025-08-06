"""
Management command to populate sample event data.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, time
import random

from events.models import Event, EventCategory


class Command(BaseCommand):
    help = 'Populate sample event data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample event data...')

        # Create event categories
        categories_data = [
            {
                'name': 'Worship Services',
                'slug': 'worship-services',
                'description': 'Regular worship services and special services',
                'color': '#0EC6EB',
                'is_active': True
            },
            {
                'name': 'Bible Study',
                'slug': 'bible-study',
                'description': 'Bible study sessions and small group meetings',
                'color': '#10B981',
                'is_active': True
            },
            {
                'name': 'Youth Ministry',
                'slug': 'youth-ministry',
                'description': 'Events and activities for young people',
                'color': '#F59E0B',
                'is_active': True
            },
            {
                'name': 'Community Outreach',
                'slug': 'community-outreach',
                'description': 'Community service and outreach programs',
                'color': '#EF4444',
                'is_active': True
            },
            {
                'name': 'Special Events',
                'slug': 'special-events',
                'description': 'Special celebrations and conferences',
                'color': '#8B5CF6',
                'is_active': True
            },
            {
                'name': 'Fellowship',
                'slug': 'fellowship',
                'description': 'Fellowship meals and social gatherings',
                'color': '#EB750E',
                'is_active': True
            }
        ]

        categories = []
        for category_data in categories_data:
            category, created = EventCategory.objects.get_or_create(
                slug=category_data['slug'],
                defaults=category_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create events
        today = timezone.now().date()
        
        events_data = [
            # Regular Weekly Services
            {
                'title': 'Saturday Morning Worship',
                'description': 'Join us for our main worship service featuring inspiring music, biblical preaching, and fellowship. All are welcome to experience God\'s love in our community.',
                'short_description': 'Main worship service with music, preaching, and fellowship',
                'category': categories[0],  # Worship Services
                'event_type': 'service',
                'start_date': today + timedelta(days=(6 - today.weekday())),  # Next Sunday
                'start_time': time(10, 0),
                'end_time': time(12, 0),
                'location_name': 'Main Sanctuary',
                'address': '123 Church Street, Accra, Ghana',
                'is_featured': True,
                'is_published': True,
                'recurrence': 'weekly'
            },
            {
                'title': 'Wednesday Bible Study',
                'description': 'Dive deeper into God\'s Word with our midweek Bible study. We explore scripture together, discuss practical applications, and grow in our faith journey.',
                'short_description': 'Midweek Bible study and prayer meeting',
                'category': categories[1],  # Bible Study
                'event_type': 'meeting',
                'start_date': today + timedelta(days=(2 - today.weekday()) % 7),  # Next Wednesday
                'start_time': time(19, 0),
                'end_time': time(20, 30),
                'location_name': 'Fellowship Hall',
                'address': '123 Church Street, Accra, Ghana',
                'is_published': True,
                'recurrence': 'weekly'
            },
            {
                'title': 'Youth Fellowship Friday',
                'description': 'Young people ages 13-25 gather for worship, games, discussions, and building lasting friendships in Christ. Come as you are!',
                'short_description': 'Weekly youth gathering with worship and activities',
                'category': categories[2],  # Youth Ministry
                'event_type': 'social',
                'start_date': today + timedelta(days=(4 - today.weekday()) % 7),  # Next Friday
                'start_time': time(18, 0),
                'end_time': time(20, 0),
                'location_name': 'Youth Center',
                'address': '123 Church Street, Accra, Ghana',
                'contact_person': 'Pastor David Wilson',
                'contact_email': 'youth@shalomgh.org',
                'is_published': True,
                'recurrence': 'weekly'
            },

            # Special Upcoming Events
            {
                'title': 'Annual Church Conference 2025',
                'description': 'Join us for our annual church conference featuring renowned speakers, workshops, and spiritual renewal. This three-day event will strengthen your faith and equip you for ministry.',
                'short_description': 'Three-day conference with speakers and workshops',
                'category': categories[4],  # Special Events
                'event_type': 'conference',
                'start_date': today + timedelta(days=21),
                'end_date': today + timedelta(days=23),
                'start_time': time(9, 0),
                'end_time': time(17, 0),
                'location_name': 'Main Sanctuary & Fellowship Hall',
                'address': '123 Church Street, Accra, Ghana',
                'requires_registration': True,
                'registration_url': 'https://example.com/register-conference',
                'max_attendees': 500,
                'registration_deadline': timezone.now() + timedelta(days=14),
                'contact_person': 'Elder Sarah Johnson',
                'contact_email': 'conference@shalomgh.org',
                'contact_phone': '+233-24-234-5678',
                'is_featured': True,
                'is_published': True,
                'meta_description': 'Join our annual church conference with renowned speakers, workshops, and spiritual renewal opportunities.'
            },
            {
                'title': 'Community Food Drive',
                'description': 'Help us serve our community by donating non-perishable food items. We\'ll be collecting donations and preparing care packages for local families in need.',
                'short_description': 'Food collection and packaging for community families',
                'category': categories[3],  # Community Outreach
                'event_type': 'outreach',
                'start_date': today + timedelta(days=14),
                'start_time': time(9, 0),
                'end_time': time(15, 0),
                'location_name': 'Church Parking Lot',
                'address': '123 Church Street, Accra, Ghana',
                'contact_person': 'Deacon Michael Brown',
                'contact_email': 'outreach@shalomgh.org',
                'is_published': True
            },
            {
                'title': 'Marriage Enrichment Workshop',
                'description': 'Strengthen your marriage with biblical principles and practical tools. This workshop is designed for married couples seeking to deepen their relationship.',
                'short_description': 'Workshop for married couples on biblical marriage principles',
                'category': categories[4],  # Special Events
                'event_type': 'workshop',
                'start_date': today + timedelta(days=28),
                'start_time': time(10, 0),
                'end_time': time(16, 0),
                'location_name': 'Fellowship Hall',
                'address': '123 Church Street, Accra, Ghana',
                'requires_registration': True,
                'registration_url': 'https://example.com/register-marriage-workshop',
                'max_attendees': 50,
                'contact_person': 'Pastor John Smith',
                'contact_email': 'pastor@shalomgh.org',
                'is_published': True
            },
            {
                'title': 'Church Picnic & Family Day',
                'description': 'Join us for a fun-filled day of fellowship, games, food, and activities for the whole family. Bring your appetite and get ready for great fellowship!',
                'short_description': 'Family-friendly picnic with games and fellowship',
                'category': categories[5],  # Fellowship
                'event_type': 'social',
                'start_date': today + timedelta(days=35),
                'start_time': time(11, 0),
                'end_time': time(16, 0),
                'location_name': 'Legon Botanical Gardens',
                'address': 'University of Ghana, Legon, Accra',
                'contact_person': 'Fellowship Committee',
                'contact_email': 'fellowship@shalomgh.org',
                'is_featured': True,
                'is_published': True
            },
            {
                'title': 'Online Prayer Meeting',
                'description': 'Join us virtually for our weekly online prayer meeting. We\'ll pray for our church, community, and world needs together.',
                'short_description': 'Virtual prayer meeting via video conference',
                'category': categories[1],  # Bible Study
                'event_type': 'meeting',
                'start_date': today + timedelta(days=7),
                'start_time': time(20, 0),
                'end_time': time(21, 0),
                'is_online': True,
                'online_link': 'https://zoom.us/j/example-meeting-id',
                'contact_person': 'Prayer Team',
                'contact_email': 'prayer@shalomgh.org',
                'is_published': True,
                'recurrence': 'weekly'
            },
            {
                'title': 'Women\'s Ministry Breakfast',
                'description': 'Ladies, join us for a special breakfast fellowship with inspiring testimonies, worship, and sisterhood. Come hungry for food and fellowship!',
                'short_description': 'Special breakfast fellowship for women',
                'category': categories[5],  # Fellowship
                'event_type': 'social',
                'start_date': today + timedelta(days=42),
                'start_time': time(8, 0),
                'end_time': time(11, 0),
                'location_name': 'Fellowship Hall',
                'address': '123 Church Street, Accra, Ghana',
                'requires_registration': True,
                'max_attendees': 100,
                'contact_person': 'Women\'s Ministry Team',
                'contact_email': 'women@shalomgh.org',
                'is_published': True
            },
            {
                'title': 'Men\'s Ministry Retreat',
                'description': 'Men, join us for a weekend retreat focused on spiritual growth, fellowship, and building godly character. Includes meals and accommodation.',
                'short_description': 'Weekend spiritual retreat for men',
                'category': categories[4],  # Special Events
                'event_type': 'special',
                'start_date': today + timedelta(days=49),
                'end_date': today + timedelta(days=50),
                'start_time': time(18, 0),
                'end_time': time(15, 0),
                'location_name': 'Mountain View Retreat Center',
                'address': 'Aburi Mountains, Eastern Region, Ghana',
                'requires_registration': True,
                'registration_url': 'https://example.com/register-mens-retreat',
                'max_attendees': 75,
                'registration_deadline': timezone.now() + timedelta(days=35),
                'contact_person': 'Men\'s Ministry Team',
                'contact_email': 'men@shalomgh.org',
                'contact_phone': '+233-24-345-6789',
                'is_featured': True,
                'is_published': True
            }
        ]

        for event_data in events_data:
            # Create unique slug for each event
            base_slug = event_data['title'].lower().replace(' ', '-').replace('\'', '')
            event_data['slug'] = f"{base_slug}-{event_data['start_date'].strftime('%Y-%m-%d')}"
            
            event, created = Event.objects.get_or_create(
                slug=event_data['slug'],
                defaults=event_data
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(categories)} categories and {len(events_data)} events'
            )
        )
