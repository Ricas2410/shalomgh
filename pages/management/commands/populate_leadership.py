"""
Management command to populate the database with sample leadership data.
"""
from django.core.management.base import BaseCommand
from pages.models import LeadershipProfile, PageContent


class Command(BaseCommand):
    help = 'Populate the database with sample leadership data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample leadership profiles...')
        
        # Create leadership profiles
        leadership_data = [
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'position': 'senior_pastor',
                'email': 'pastor.john@shalomgh.org',
                'phone': '+233-20-123-4567',
                'bio': '''Pastor John Smith has been serving as Senior Pastor of Seventh Day Sabbath Church Of Christ since 2010. 
                
He holds a Master of Divinity from Andrews University and has over 20 years of pastoral experience. Pastor John is passionate about expository preaching, discipleship, and missions.

He is married to Sarah and they have three children: David, Ruth, and Samuel. In his free time, Pastor John enjoys reading, hiking, and spending time with his family.

Pastor John's heart is to see people come to know Jesus Christ as their personal Savior and to grow in their relationship with Him through the study of God's Word.''',
                'display_order': 1,
                'show_on_homepage': True,
                'is_active': True,
            },
            {
                'first_name': 'Michael',
                'last_name': 'Johnson',
                'position': 'associate_pastor',
                'email': 'pastor.michael@shalomgh.org',
                'phone': '+233-20-234-5678',
                'bio': '''Pastor Michael Johnson joined our church family in 2015 as Associate Pastor. He assists in pastoral duties, preaching, and oversees our youth and young adult ministries.

Pastor Michael graduated from Oakwood University with a degree in Theology and has a heart for reaching the next generation for Christ. He is known for his dynamic preaching style and his ability to connect with people of all ages.

He is married to Grace and they have two young children. Pastor Michael enjoys playing basketball, music, and mentoring young people in their faith journey.''',
                'display_order': 2,
                'show_on_homepage': True,
                'is_active': True,
            },
            {
                'first_name': 'David',
                'last_name': 'Williams',
                'position': 'elder',
                'email': 'elder.david@shalomgh.org',
                'phone': '+233-20-345-6789',
                'bio': '''Elder David Williams has been a faithful member of our church for over 15 years and has served as an elder for the past 8 years. He provides spiritual oversight and guidance to our congregation.

David works as a school principal and brings his leadership experience to his church service. He is passionate about Christian education and family ministry.

He is married to Mary and they have four children. Elder David enjoys reading, gardening, and spending time with his grandchildren.''',
                'display_order': 3,
                'show_on_homepage': True,
                'is_active': True,
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Thompson',
                'position': 'worship_leader',
                'email': 'worship@shalomgh.org',
                'phone': '+233-20-456-7890',
                'bio': '''Sarah Thompson has been leading worship at our church for over 6 years. She has a beautiful voice and a heart for worship that inspires our congregation to enter into God's presence.

Sarah studied music at the University of Ghana and has been involved in church music ministry for over 10 years. She leads our worship team and coordinates all musical elements of our services.

She is married to James and they have two children. Sarah enjoys singing, playing piano, and teaching music to children in our community.''',
                'display_order': 4,
                'show_on_homepage': True,
                'is_active': True,
            },
            {
                'first_name': 'Robert',
                'last_name': 'Brown',
                'position': 'deacon',
                'email': 'deacon.robert@shalomgh.org',
                'phone': '+233-20-567-8901',
                'bio': '''Deacon Robert Brown has been serving our church faithfully for over 12 years. He oversees our community outreach programs and assists with the practical needs of our congregation.

Robert works as a social worker and brings his passion for helping others to his church service. He coordinates our food bank, clothing drive, and other community service initiatives.

He is married to Linda and they have three children. Deacon Robert enjoys volunteering, sports, and spending time with his family.''',
                'display_order': 5,
                'show_on_homepage': False,
                'is_active': True,
            },
            {
                'first_name': 'Grace',
                'last_name': 'Davis',
                'position': 'ministry_leader',
                'custom_position': 'Women\'s Ministry Leader',
                'email': 'womens.ministry@shalomgh.org',
                'phone': '+233-20-678-9012',
                'bio': '''Grace Davis leads our Women's Ministry and has been instrumental in creating programs that encourage and support the women in our church family.

She organizes Bible studies, retreats, and fellowship events that help women grow in their faith and build meaningful relationships. Grace has a heart for mentoring younger women and helping them discover their gifts and calling.

She is married to Peter and they have two teenage daughters. Grace enjoys cooking, crafting, and hosting gatherings in her home.''',
                'display_order': 6,
                'show_on_homepage': False,
                'is_active': True,
            },
        ]
        
        created_count = 0
        for data in leadership_data:
            profile, created = LeadershipProfile.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created: {profile.get_full_name()}')
            else:
                self.stdout.write(f'Already exists: {profile.get_full_name()}')
        
        self.stdout.write(f'Created {created_count} new leadership profiles.')
        
        # Create page content
        self.stdout.write('Creating sample page content...')
        
        page_content_data = [
            {
                'page': 'about',
                'title': 'Welcome to Our Church Family',
                'content': '''We are a vibrant community of believers committed to following Jesus Christ and making disciples. Our church has been serving the community for over 35 years, and we continue to grow in faith, love, and service.

Our mission is to glorify God through worship, discipleship, fellowship, and service. We believe in the power of God's Word to transform lives and communities, and we are passionate about sharing the Gospel with everyone we meet.

Whether you're new to faith or have been walking with God for years, we invite you to join our church family. Together, we can grow in our relationship with Jesus Christ and make a positive impact in our community and around the world.''',
                'is_published': True,
            },
            {
                'page': 'our_story',
                'title': 'Our Journey of Faith',
                'content': '''The Seventh Day Sabbath Church Of Christ began in 1985 when a small group of 15 families felt called by God to establish a church that would faithfully preach His Word and serve the community with love and compassion.

From humble beginnings meeting in a rented community center, God has blessed our church to grow into a thriving congregation of over 500 members. Throughout our journey, we have remained committed to our founding principles: biblical truth, authentic worship, and compassionate service.

Over the years, we have seen God work in amazing ways through our church family. We have sent missionaries around the world, established community programs that serve thousands of people, and witnessed countless lives transformed by the power of the Gospel.

Today, we continue to build on the foundation laid by our founding members, always seeking to honor God and serve others with excellence and integrity.''',
                'is_published': True,
            },
            {
                'page': 'beliefs',
                'title': 'Our Statement of Faith',
                'content': '''We believe in the fundamental truths of Christianity as revealed in the Holy Scriptures. Our faith is built on the solid foundation of God's Word, and these beliefs guide everything we do as a church family.

The Bible is our final authority in all matters of faith and practice. We believe in the Trinity - one God eternally existing in three persons: Father, Son, and Holy Spirit. We believe that Jesus Christ is both fully God and fully man, and that salvation comes through faith in Him alone.

As a Seventh Day Sabbath Church, we observe the Sabbath from Friday evening to Saturday  evening as a holy day of rest, worship, and spiritual renewal. We believe this is God's gift to humanity and a sign of our covenant relationship with Him.

We are committed to living out these beliefs in practical ways through our worship, fellowship, service, and witness to the world around us.''',
                'is_published': True,
            },
        ]
        
        content_created_count = 0
        for data in page_content_data:
            content, created = PageContent.objects.get_or_create(
                page=data['page'],
                defaults=data
            )
            if created:
                content_created_count += 1
                self.stdout.write(f'Created page content: {data["page"]}')
            else:
                self.stdout.write(f'Page content already exists: {data["page"]}')
        
        self.stdout.write(f'Created {content_created_count} new page content entries.')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with {created_count} leadership profiles '
                f'and {content_created_count} page content entries.'
            )
        )
