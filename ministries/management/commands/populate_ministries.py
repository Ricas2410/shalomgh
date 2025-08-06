"""
Management command to populate sample ministry data.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from ministries.models import Ministry, MinistryGallery
from pages.models import LeadershipProfile


class Command(BaseCommand):
    help = 'Populate sample ministry data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting ministry data population...'))
        
        # Get some leadership profiles for ministry leaders
        leaders = list(LeadershipProfile.objects.all())
        
        # Sample ministry data
        ministries_data = [
            {
                'name': 'Youth Ministry',
                'ministry_type': 'youth',
                'short_description': 'Empowering young people to grow in faith and leadership through engaging activities and biblical teaching.',
                'description': '''Our Youth Ministry is dedicated to helping teenagers and young adults develop a strong relationship with Jesus Christ. We provide a safe and welcoming environment where young people can ask questions, explore their faith, and build lasting friendships.

Through weekly meetings, special events, and service projects, we aim to equip our youth with the tools they need to navigate life's challenges while staying grounded in biblical principles.''',
                'mission_statement': 'To raise up a generation of young leaders who are passionate about God, committed to His Word, and ready to make a positive impact in their communities.',
                'activities': '''• Weekly youth group meetings every Friday evening
• Monthly outreach events and community service projects
• Annual youth camp and retreat weekends
• Leadership development programs
• Mentorship opportunities with adult leaders
• Sports and recreational activities
• Bible study groups and discipleship classes''',
                'requirements': 'Open to all young people ages 13-25. Regular attendance and participation in activities is encouraged.',
                'min_age': 13,
                'max_age': 25,
                'meeting_day': 'Friday',
                'meeting_time': '7:00 PM - 9:00 PM',
                'meeting_location': 'Youth Center',
                'contact_email': 'youth@shalomgh.org',
                'contact_phone': '+233 24 123 4567',
                'is_featured': True,
                'is_active': True,
                'display_order': 1,
            },
            {
                'name': "Women's Fellowship",
                'ministry_type': 'womens',
                'short_description': 'A supportive community where women can grow spiritually, build friendships, and serve together.',
                'description': '''The Women\'s Fellowship provides a nurturing environment for women of all ages to come together in prayer, study, and fellowship. We believe in the power of women supporting women in their spiritual journey.

Our ministry focuses on biblical womanhood, practical life skills, and creating opportunities for service within the church and community.''',
                'mission_statement': 'To encourage and equip women to live out their faith boldly while supporting one another through all seasons of life.',
                'activities': '''• Monthly fellowship meetings with guest speakers
• Bible study groups and book clubs
• Prayer circles and intercessory prayer ministry
• Community service and outreach projects
• Mentorship programs for young women
• Special events and retreats
• Craft workshops and skill-sharing sessions''',
                'requirements': 'Open to all women. Newcomers are always welcome.',
                'min_age': 18,
                'max_age': None,
                'meeting_day': 'Second Saturday ',
                'meeting_time': '10:00 AM - 12:00 PM',
                'meeting_location': 'Fellowship Hall',
                'contact_email': 'women@shalomgh.org',
                'contact_phone': '+233 24 234 5678',
                'is_featured': True,
                'is_active': True,
                'display_order': 2,
            },
            {
                'name': "Men's Brotherhood",
                'ministry_type': 'mens',
                'short_description': 'Building strong Christian men through fellowship, accountability, and service.',
                'description': '''The Men\'s Brotherhood is committed to helping men grow in their relationship with God and become the leaders He has called them to be in their homes, workplaces, and communities.

We focus on biblical masculinity, leadership development, and creating strong bonds of brotherhood among the men of our church.''',
                'mission_statement': 'To develop godly men who lead with integrity, serve with humility, and love with Christ\'s heart.',
                'activities': '''• Monthly breakfast meetings with devotional messages
• Men\'s Bible study groups
• Service projects and community outreach
• Mentorship and accountability partnerships
• Annual men\'s retreat and camping trips
• Sports activities and recreational events
• Prayer meetings and spiritual warfare training''',
                'requirements': 'Open to all men 18 years and older.',
                'min_age': 18,
                'max_age': None,
                'meeting_day': 'First Saturday ',
                'meeting_time': '7:00 AM - 9:00 AM',
                'meeting_location': 'Men\'s Hall',
                'contact_email': 'men@shalomgh.org',
                'contact_phone': '+233 24 345 6789',
                'is_featured': False,
                'is_active': True,
                'display_order': 3,
            },
            {
                'name': "Children's Ministry",
                'ministry_type': 'children',
                'short_description': 'Nurturing young hearts to know and love Jesus through age-appropriate teaching and activities.',
                'description': '''Our Children\'s Ministry is designed to introduce children to the love of Jesus Christ in a fun, safe, and engaging environment. We believe that children are not just the church of tomorrow, but an important part of the church today.

Through creative teaching methods, interactive activities, and loving care, we help children develop a strong foundation of faith that will last a lifetime.''',
                'mission_statement': 'To partner with parents in raising children who know Jesus, love others, and live out their faith with joy and confidence.',
                'activities': '''• Saturday School classes for different age groups
• Vacation Bible School during school holidays
• Children\'s choir and drama presentations
• Bible memory verse competitions
• Craft activities and creative learning
• Special children\'s events and parties
• Parent-child activities and family events''',
                'requirements': 'Open to children ages 3-12. Parent participation is encouraged.',
                'min_age': 3,
                'max_age': 12,
                'meeting_day': 'Sunday',
                'meeting_time': '9:00 AM - 10:30 AM',
                'meeting_location': 'Children\'s Wing',
                'contact_email': 'children@shalomgh.org',
                'contact_phone': '+233 24 456 7890',
                'is_featured': True,
                'is_active': True,
                'display_order': 4,
            },
            {
                'name': 'Worship Team',
                'ministry_type': 'music',
                'short_description': 'Leading the congregation in heartfelt worship through music and song.',
                'description': '''The Worship Team is passionate about creating an atmosphere where people can encounter God through music and worship. We believe that worship is not just about the songs we sing, but about the heart behind the music.

Our team consists of vocalists, instrumentalists, and technical support members who work together to facilitate meaningful worship experiences during our services and special events.''',
                'mission_statement': 'To lead people into the presence of God through authentic, Spirit-led worship that glorifies Jesus Christ.',
                'activities': '''• Leading worship during Saturday services
• Special music for church events and celebrations
• Worship team training and development
• Recording ministry for online services
• Community concerts and outreach events
• Instrument lessons and music education
• Prayer and worship nights''',
                'requirements': 'Musical ability and a heart for worship. Auditions may be required for certain positions.',
                'min_age': 16,
                'max_age': None,
                'meeting_day': 'Thursday',
                'meeting_time': '7:00 PM - 9:00 PM',
                'meeting_location': 'Sanctuary',
                'contact_email': 'worship@shalomgh.org',
                'contact_phone': '+233 24 567 8901',
                'is_featured': False,
                'is_active': True,
                'display_order': 5,
            },
            {
                'name': 'Prayer Ministry',
                'ministry_type': 'prayer',
                'short_description': 'Interceding for our church, community, and world through dedicated prayer.',
                'description': '''The Prayer Ministry is the spiritual backbone of our church, committed to seeking God\'s face and interceding for the needs of our congregation and community. We believe in the power of prayer to transform lives and situations.

Our ministry provides opportunities for both corporate and individual prayer, training in different prayer methods, and support for those seeking prayer.''',
                'mission_statement': 'To create a culture of prayer that seeks God\'s will and releases His power in our church and community.',
                'activities': '''• Weekly prayer meetings and intercession sessions
• Prayer chains for urgent needs and requests
• Prayer walking in the community
• Fasting and prayer events
• Prayer training and workshops
• 24-hour prayer vigils
• Prayer support for church events and ministries''',
                'requirements': 'A heart for prayer and commitment to regular participation.',
                'min_age': 16,
                'max_age': None,
                'meeting_day': 'Wednesday',
                'meeting_time': '6:00 AM - 7:00 AM',
                'meeting_location': 'Prayer Room',
                'contact_email': 'prayer@shalomgh.org',
                'contact_phone': '+233 24 678 9012',
                'is_featured': False,
                'is_active': True,
                'display_order': 6,
            },
            {
                'name': 'Evangelism & Outreach',
                'ministry_type': 'evangelism',
                'short_description': 'Sharing the Gospel and serving our community with the love of Christ.',
                'description': '''The Evangelism & Outreach Ministry is dedicated to fulfilling the Great Commission by sharing the Gospel message and demonstrating God\'s love through practical service to our community.

We organize various outreach activities, community service projects, and evangelistic events to reach people with the good news of Jesus Christ.''',
                'mission_statement': 'To be the hands and feet of Jesus in our community, sharing His love through word and deed.',
                'activities': '''• Community outreach events and street evangelism
• Food distribution and charity drives
• Hospital and prison visitation programs
• Neighborhood cleanup and service projects
• Evangelism training and equipping sessions
• Mission trips and cross-cultural outreach
• Partnership with local charities and organizations''',
                'requirements': 'A heart for the lost and willingness to step out of your comfort zone.',
                'min_age': 16,
                'max_age': None,
                'meeting_day': 'Saturday ',
                'meeting_time': '9:00 AM - 12:00 PM',
                'meeting_location': 'Community Center',
                'contact_email': 'outreach@shalomgh.org',
                'contact_phone': '+233 24 789 0123',
                'is_featured': False,
                'is_active': True,
                'display_order': 7,
            },
            {
                'name': 'Discipleship Groups',
                'ministry_type': 'discipleship',
                'short_description': 'Growing deeper in faith through small group Bible study and mentorship.',
                'description': '''Our Discipleship Groups provide intimate settings for spiritual growth through Bible study, prayer, and mutual encouragement. These small groups meet regularly to study God\'s Word and apply its truths to daily life.

We believe that spiritual growth happens best in the context of authentic relationships where people can share their struggles, celebrate victories, and grow together in faith.''',
                'mission_statement': 'To make disciples who make disciples, creating a multiplication of spiritual growth throughout our church.',
                'activities': '''• Weekly small group Bible studies
• Discipleship training and mentorship programs
• Book studies and topical discussions
• Prayer and accountability partnerships
• Service projects as a group
• Social activities and fellowship events
• Leadership development for group facilitators''',
                'requirements': 'Commitment to regular attendance and participation in group activities.',
                'min_age': 18,
                'max_age': None,
                'meeting_day': 'Various',
                'meeting_time': 'Various times',
                'meeting_location': 'Various homes',
                'contact_email': 'discipleship@shalomgh.org',
                'contact_phone': '+233 24 890 1234',
                'is_featured': False,
                'is_active': True,
                'display_order': 8,
            },
        ]
        
        # Create ministries
        created_count = 0
        for ministry_data in ministries_data:
            # Assign a leader if available
            if leaders:
                ministry_data['leader'] = leaders[created_count % len(leaders)]
            
            ministry_data['slug'] = slugify(ministry_data['name'])
            
            ministry, created = Ministry.objects.get_or_create(
                slug=ministry_data['slug'],
                defaults=ministry_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created ministry: {ministry.name}')
                
                # Add assistant leaders if available
                if len(leaders) > 1:
                    assistant_leaders = leaders[1:min(3, len(leaders))]
                    ministry.assistant_leaders.set(assistant_leaders)
            else:
                self.stdout.write(f'Ministry already exists: {ministry.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} ministries. '
                f'Total ministries in database: {Ministry.objects.count()}'
            )
        )
