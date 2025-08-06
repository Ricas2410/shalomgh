"""
Management command to populate sample sermon data.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random

from sermons.models import Speaker, SermonSeries, Sermon
from pages.models import LeadershipProfile


class Command(BaseCommand):
    help = 'Populate sample sermon data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample sermon data...')

        # Create speakers (linked to existing leadership profiles)
        speakers_data = [
            {
                'name': 'Pastor John Smith',
                'bio': 'Pastor John has been serving our congregation for over 15 years. He holds a Master of Divinity from Seminary College and is passionate about expository preaching and discipleship.',
                'slug': 'pastor-john-smith'
            },
            {
                'name': 'Elder Sarah Johnson',
                'bio': 'Elder Sarah brings a heart for worship and biblical teaching. She has been in ministry for 10 years and specializes in women\'s ministry and family counseling.',
                'slug': 'elder-sarah-johnson'
            },
            {
                'name': 'Deacon Michael Brown',
                'bio': 'Deacon Michael serves with dedication in both preaching and community outreach. His messages focus on practical Christian living and social justice.',
                'slug': 'deacon-michael-brown'
            },
            {
                'name': 'Pastor David Wilson',
                'bio': 'Pastor David is our youth pastor who also preaches regularly. He has a gift for making biblical truths relevant to all ages and backgrounds.',
                'slug': 'pastor-david-wilson'
            }
        ]

        speakers = []
        for speaker_data in speakers_data:
            speaker, created = Speaker.objects.get_or_create(
                slug=speaker_data['slug'],
                defaults=speaker_data
            )
            speakers.append(speaker)
            if created:
                self.stdout.write(f'Created speaker: {speaker.name}')

        # Create sermon series
        series_data = [
            {
                'title': 'Walking in Faith',
                'description': 'A comprehensive study on what it means to live by faith in our daily lives. This series explores biblical examples of faith and how we can apply these lessons today.',
                'slug': 'walking-in-faith',
                'start_date': datetime(2024, 1, 7).date(),
                'end_date': datetime(2024, 2, 25).date(),
                'is_featured': True,
                'is_active': True
            },
            {
                'title': 'The Heart of Worship',
                'description': 'Discover the true meaning of worship and how it transforms our relationship with God. Learn about worship in spirit and truth.',
                'slug': 'heart-of-worship',
                'start_date': datetime(2024, 3, 3).date(),
                'end_date': datetime(2024, 4, 21).date(),
                'is_featured': True,
                'is_active': True
            },
            {
                'title': 'Living as Light',
                'description': 'Jesus called us to be the light of the world. This series examines how Christians can shine God\'s light in a dark world.',
                'slug': 'living-as-light',
                'start_date': datetime(2024, 5, 5).date(),
                'end_date': datetime(2024, 6, 23).date(),
                'is_featured': False,
                'is_active': True
            },
            {
                'title': 'Psalms of Praise',
                'description': 'Journey through selected Psalms and discover the power of praise and worship in the life of a believer.',
                'slug': 'psalms-of-praise',
                'start_date': datetime(2024, 7, 7).date(),
                'end_date': datetime(2024, 8, 25).date(),
                'is_featured': True,
                'is_active': True
            },
            {
                'title': 'Kingdom Principles',
                'description': 'Learn about the principles that govern God\'s kingdom and how to live as citizens of heaven while on earth.',
                'slug': 'kingdom-principles',
                'start_date': datetime(2024, 9, 1).date(),
                'end_date': datetime(2024, 10, 27).date(),
                'is_featured': False,
                'is_active': True
            }
        ]

        series_list = []
        for series_data in series_data:
            series, created = SermonSeries.objects.get_or_create(
                slug=series_data['slug'],
                defaults=series_data
            )
            series_list.append(series)
            if created:
                self.stdout.write(f'Created series: {series.title}')

        # Create sermons
        sermons_data = [
            # Walking in Faith Series
            {
                'title': 'Faith That Moves Mountains',
                'description': 'Exploring Jesus\' teaching about faith that can move mountains and how this applies to our spiritual journey.',
                'speaker': speakers[0],
                'series': series_list[0],
                'date_preached': datetime(2024, 1, 7).date(),
                'scripture_references': 'Matthew 17:20, Mark 11:22-24, Hebrews 11:1-6',
                'media_type': 'both',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'Faith is not just belief, but active trust in God\'s promises. When we align our hearts with God\'s will, our faith becomes a powerful force for His kingdom.',
                'tags': 'faith, prayer, trust, mountains, miracles',
                'is_featured': True,
                'is_published': True,
                'view_count': 245,
                'download_count': 67
            },
            {
                'title': 'Abraham\'s Journey of Faith',
                'description': 'Learning from Abraham\'s example of faith as he followed God\'s call to leave everything behind.',
                'speaker': speakers[1],
                'series': series_list[0],
                'date_preached': datetime(2024, 1, 14).date(),
                'scripture_references': 'Genesis 12:1-9, Romans 4:16-25, Hebrews 11:8-12',
                'media_type': 'video',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'Abraham\'s faith was demonstrated through obedience. He didn\'t know where he was going, but he knew who was leading him.',
                'tags': 'Abraham, obedience, calling, promise, journey',
                'is_featured': False,
                'is_published': True,
                'view_count': 189,
                'download_count': 43
            },
            {
                'title': 'Faith in Times of Trial',
                'description': 'How to maintain faith when facing difficult circumstances and seemingly impossible situations.',
                'speaker': speakers[2],
                'series': series_list[0],
                'date_preached': datetime(2024, 1, 21).date(),
                'scripture_references': 'Job 13:15, Romans 8:28, James 1:2-4',
                'media_type': 'both',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'Trials test our faith but also strengthen it. God uses difficult times to develop our character and deepen our trust in Him.',
                'tags': 'trials, suffering, perseverance, character, trust',
                'is_featured': True,
                'is_published': True,
                'view_count': 312,
                'download_count': 89
            },

            # Heart of Worship Series
            {
                'title': 'Worship in Spirit and Truth',
                'description': 'Understanding what Jesus meant when He spoke about worshiping in spirit and truth.',
                'speaker': speakers[0],
                'series': series_list[1],
                'date_preached': datetime(2024, 3, 3).date(),
                'scripture_references': 'John 4:19-26, Psalm 95:1-7, Romans 12:1-2',
                'media_type': 'both',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'True worship goes beyond external expressions to the condition of our hearts. It\'s about surrendering our whole lives to God.',
                'tags': 'worship, spirit, truth, surrender, heart',
                'is_featured': True,
                'is_published': True,
                'view_count': 278,
                'download_count': 72
            },
            {
                'title': 'The Sacrifice of Praise',
                'description': 'Learning to offer praise to God even in difficult circumstances, following biblical examples.',
                'speaker': speakers[3],
                'series': series_list[1],
                'date_preached': datetime(2024, 3, 10).date(),
                'scripture_references': 'Hebrews 13:15, Psalm 50:14, Acts 16:25-26',
                'media_type': 'audio',
                'notes': 'Praise is not dependent on our circumstances but on God\'s character. When we praise God in trials, we demonstrate our faith.',
                'tags': 'praise, sacrifice, circumstances, character, demonstration',
                'is_featured': False,
                'is_published': True,
                'view_count': 156,
                'download_count': 34
            },

            # Living as Light Series
            {
                'title': 'You Are the Light of the World',
                'description': 'Exploring Jesus\' declaration that His followers are the light of the world and what this means for us today.',
                'speaker': speakers[1],
                'series': series_list[2],
                'date_preached': datetime(2024, 5, 5).date(),
                'scripture_references': 'Matthew 5:14-16, John 8:12, Ephesians 5:8-14',
                'media_type': 'both',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'As believers, we carry the light of Christ within us. Our lives should reflect His love and truth to a world in darkness.',
                'tags': 'light, world, witness, reflection, darkness',
                'is_featured': True,
                'is_published': True,
                'view_count': 203,
                'download_count': 56
            },

            # Individual sermons (not part of series)
            {
                'title': 'The Power of Prayer',
                'description': 'Understanding the importance and effectiveness of prayer in the life of a believer.',
                'speaker': speakers[2],
                'series': None,
                'date_preached': datetime(2024, 11, 3).date(),
                'scripture_references': 'Matthew 6:5-15, Luke 18:1-8, James 5:16',
                'media_type': 'both',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'Prayer is our direct line of communication with God. It\'s not just asking for things, but building a relationship with our Heavenly Father.',
                'tags': 'prayer, communication, relationship, power, effectiveness',
                'is_featured': True,
                'is_published': True,
                'view_count': 334,
                'download_count': 98
            },
            {
                'title': 'Love Your Neighbor',
                'description': 'Practical ways to show Christ\'s love to those around us in our daily lives.',
                'speaker': speakers[3],
                'series': None,
                'date_preached': datetime(2024, 10, 27).date(),
                'scripture_references': 'Matthew 22:37-39, Luke 10:25-37, 1 John 4:7-21',
                'media_type': 'video',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'Loving our neighbor is not just a suggestion but a commandment. It\'s how the world will know we are His disciples.',
                'tags': 'love, neighbor, commandment, disciples, practical',
                'is_featured': False,
                'is_published': True,
                'view_count': 167,
                'download_count': 41
            },
            {
                'title': 'The Great Commission',
                'description': 'Understanding our calling to make disciples and share the Gospel with all nations.',
                'speaker': speakers[0],
                'series': None,
                'date_preached': datetime(2024, 10, 20).date(),
                'scripture_references': 'Matthew 28:16-20, Acts 1:8, Romans 10:14-15',
                'media_type': 'both',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'The Great Commission is not just for missionaries but for every believer. We are all called to be witnesses of Christ\'s love.',
                'tags': 'commission, disciples, gospel, nations, witnesses',
                'is_featured': False,
                'is_published': True,
                'view_count': 198,
                'download_count': 52
            },
            {
                'title': 'Thanksgiving and Gratitude',
                'description': 'Cultivating a heart of thanksgiving and understanding the biblical importance of gratitude.',
                'speaker': speakers[1],
                'series': None,
                'date_preached': datetime(2024, 11, 24).date(),
                'scripture_references': '1 Thessalonians 5:18, Psalm 100, Colossians 3:15-17',
                'media_type': 'both',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'notes': 'Gratitude transforms our perspective and draws us closer to God. In everything, we can find reasons to give thanks.',
                'tags': 'thanksgiving, gratitude, perspective, transformation, praise',
                'is_featured': True,
                'is_published': True,
                'view_count': 289,
                'download_count': 76
            }
        ]

        for sermon_data in sermons_data:
            sermon, created = Sermon.objects.get_or_create(
                title=sermon_data['title'],
                speaker=sermon_data['speaker'],
                date_preached=sermon_data['date_preached'],
                defaults=sermon_data
            )
            if created:
                self.stdout.write(f'Created sermon: {sermon.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(speakers)} speakers, '
                f'{len(series_list)} series, and {len(sermons_data)} sermons'
            )
        )
