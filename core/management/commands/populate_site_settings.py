"""
Management command to populate site settings with realistic data.
"""
from django.core.management.base import BaseCommand
from core.models import SiteSetting


class Command(BaseCommand):
    help = 'Populate site settings with realistic data'

    def handle(self, *args, **options):
        """Populate site settings."""
        self.stdout.write('Populating site settings...')
        
        # Get or create site settings
        settings = SiteSetting.get_settings()
        
        # Update site information
        settings.site_name = 'ShalomGH'
        settings.church_name = 'Seventh Day Sabbath Church Of Christ'
        settings.tagline = 'A Community of Faith, Hope, and Love'
        settings.welcome_message = (
            'Welcome to Seventh Day Sabbath Church Of Christ! We are a vibrant community '
            'of believers committed to following Jesus Christ and living according to His Word. '
            'Whether you\'re seeking spiritual growth, community fellowship, or answers to life\'s '
            'big questions, we invite you to join us on this journey of faith.'
        )
        
        # Contact information
        settings.phone = '(233) 555-0123'
        settings.email = 'info@shalomgh.com'
        settings.address = (
            'Seventh Day Sabbath Church Of Christ\n'
            '123 Faith Avenue\n'
            'Accra, Greater Accra Region\n'
            'Ghana'
        )
        
        # Service times in HTML format
        settings.service_times = '''
        <div class="space-y-2">
            <div class="flex justify-between">
                <span>Saturday  Sabbath Worship</span>
                <span>10:00 AM - 12:00 PM</span>
            </div>
            <div class="flex justify-between">
                <span>Wednesday Bible Study</span>
                <span>7:00 PM - 8:30 PM</span>
            </div>
            <div class="flex justify-between">
                <span>Friday Prayer Meeting</span>
                <span>7:00 PM - 8:00 PM</span>
            </div>
            <div class="flex justify-between">
                <span>Youth Fellowship</span>
                <span>Saturday  2:00 PM - 4:00 PM</span>
            </div>
        </div>
        '''
        
        # External URLs (placeholder for now)
        settings.member_portal_url = 'https://members.shalomgh.com'
        settings.giving_platform_url = 'https://giving.shalomgh.com'
        
        # Social media URLs
        settings.facebook_url = 'https://facebook.com/shalomgh'
        settings.twitter_url = 'https://twitter.com/shalomgh'
        settings.instagram_url = 'https://instagram.com/shalomgh'
        settings.youtube_url = 'https://youtube.com/@shalomgh'
        
        # SEO settings
        settings.meta_description = (
            'Seventh Day Sabbath Church Of Christ in Accra, Ghana. Join our community '
            'of faith for worship, Bible study, and fellowship. All are welcome!'
        )
        settings.meta_keywords = (
            'Seventh Day Sabbath Church, Accra church, Ghana church, Christian community, '
            'Bible study, worship, fellowship, faith, Jesus Christ, Sabbath worship'
        )
        
        # Google services (placeholder API keys)
        settings.google_maps_api_key = ''  # To be configured by admin
        settings.google_analytics_id = ''  # To be configured by admin
        
        # Save the settings
        settings.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated site settings for {settings.church_name}'
            )
        )
        
        # Display summary
        self.stdout.write('\nSite Settings Summary:')
        self.stdout.write(f'  Site Name: {settings.site_name}')
        self.stdout.write(f'  Church Name: {settings.church_name}')
        self.stdout.write(f'  Phone: {settings.phone}')
        self.stdout.write(f'  Email: {settings.email}')
        self.stdout.write(f'  Address: {settings.address.replace(chr(10), ", ")}')
        self.stdout.write(f'  Facebook: {settings.facebook_url}')
        self.stdout.write(f'  Instagram: {settings.instagram_url}')
        self.stdout.write('\nNote: Configure Google Maps API key and Analytics ID in admin for full functionality.')
