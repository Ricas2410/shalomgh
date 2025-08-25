from django.db import migrations
from django.utils.text import slugify


def seed_default_ministries(apps, schema_editor):
    Ministry = apps.get_model('ministries', 'Ministry')

    defaults = [
        {
            'name': 'Pastoral Council',
            'ministry_type': 'other',
            'short_description': 'Providing spiritual oversight, prayer support, and shepherding for the entire church family.',
            'description': (
                'The Pastoral Council is the spiritual heart of the church. This ministry offers leadership, '
                'guidance, and covering through prayer, teaching, and mentoring. They focus on equipping believers '
                'to grow in Christ, preserving sound doctrine, and nurturing discipleship at every level. '
                'In addition, the Council provides pastoral care, encouragement, and counsel to individuals and families, '
                'ensuring that the church remains firmly rooted in the Word of God while advancing its mission. '
                'The Pastoral Council also coordinates training for leaders, supports missions, and serves as a pillar '
                'of wisdom for the congregation.'
            ),
            'mission_statement': 'To shepherd the flock of Christ faithfully, with integrity, wisdom, and prayerful leadership.',
            'meeting_day': 'Monthly',
            'meeting_time': 'Varies',
            'meeting_location': 'Church Conference Room',
            'display_order': 1,
        },
        {
            'name': 'Youth Fellowship',
            'ministry_type': 'youth',
            'short_description': 'Equipping teens and young adults to live boldly for Christ in their schools, communities, and future callings.',
            'description': (
                'Youth Fellowship is a vibrant community designed for teenagers and young adults who desire to grow in '
                'faith and character. Through dynamic Bible studies, mentorship, interactive discussions, worship, and '
                'creative activities, the Youth Fellowship provides a safe space to ask questions, build godly friendships, '
                'and discover purpose. Members are challenged to live counter-culturally for Jesus, using their gifts to serve '
                'both the church and society. The fellowship also organizes camps, evangelism, skill-development workshops, '
                'and outreach programs that prepare the next generation of leaders to impact the world for Christ.'
            ),
            'mission_statement': 'To disciple and empower young people with truth, character, and passion for God and others.',
            'meeting_day': 'Fridays',
            'meeting_time': '6:00 PM - 8:00 PM',
            'meeting_location': 'Youth Hall',
            'min_age': 13,
            'max_age': 25,
            'display_order': 2,
        },
        {
            'name': "Women Fellowship",
            'ministry_type': 'womens',
            'short_description': 'Bringing women together in prayer, discipleship, and service to strengthen families, church, and community.',
            'description': (
                'Women Fellowship is a ministry that nurtures and empowers women to live as godly role models in the home, '
                'church, and society. It is a gathering of women of all ages who pray together, study the Scriptures, and offer '
                'mentorship and support to one another. Through fellowship meetings, retreats, workshops, and outreach programs, '
                'members are encouraged to grow spiritually, emotionally, and socially. Women Fellowship also leads various charitable '
                'initiatives, supporting widows, single mothers, and the less privileged while fostering unity and sisterhood.'
            ),
            'mission_statement': 'To cultivate godly women who reflect Christ in every sphere of life and influence others with grace.',
            'meeting_day': 'Saturdays',
            'meeting_time': '4:00 PM - 6:00 PM',
            'meeting_location': 'Main Auditorium',
            'display_order': 3,
        },
        {
            'name': 'Children Ministry',
            'ministry_type': 'children',
            'short_description': 'Nurturing children with biblical foundations, teaching them to love Jesus and follow His ways.',
            'description': (
                'Children Ministry partners with parents and guardians to raise children who know and love Jesus from an early age. '
                'Through age-appropriate Bible lessons, storytelling, worship, crafts, and interactive games, children are introduced '
                'to the gospel in a joyful and engaging way. The ministry creates a safe, fun, and spiritually nourishing environment '
                'where children grow in knowledge, build character, and develop a personal relationship with Christ. It also provides '
                'special programs such as vacation Bible schools, children’s camps, and drama presentations to enhance learning.'
            ),
            'mission_statement': 'To lay strong spiritual foundations in children and raise young disciples who delight in God and His Word.',
            'meeting_day': 'Sundays',
            'meeting_time': 'During Services',
            'meeting_location': 'Children’s Classrooms',
            'min_age': 0,
            'max_age': 12,
            'display_order': 4,
        },
        {
            'name': 'Singing Band',
            'ministry_type': 'music',
            'short_description': 'Leading the congregation in joyful, Christ-centered worship and ministering through music.',
            'description': (
                'The Singing Band serves as a worship ministry, using music to glorify God and lead the congregation into His presence. '
                'This ministry supports all church services, evangelistic outreaches, and special events through song and praise. Members '
                'are trained to steward their musical gifts with humility and excellence while ministering with passion and unity. '
                'The Singing Band also collaborates with other music ministries, organizes rehearsals, and produces songs that uplift and '
                'inspire believers in their walk with Christ.'
            ),
            'mission_statement': 'To glorify God by leading His people in heartfelt praise and worship through the gift of music.',
            'meeting_day': 'Thursdays',
            'meeting_time': '6:30 PM - 8:30 PM',
            'meeting_location': 'Sanctuary',
            'display_order': 5,
        },
        {
            'name': 'Deacons Council',
            'ministry_type': 'other',
            'short_description': 'Overseeing practical service, member care, and logistics to support the smooth running of church life.',
            'description': (
                'The Deacons Council is dedicated to serving the practical needs of the church family. They coordinate logistics, '
                'manage church facilities, and provide support for various functions and programs. The Deacons also play a key role '
                'in caring for members in need, offering help, encouragement, and tangible support. They embody servant leadership, '
                'modeling integrity, humility, and faithfulness while partnering with pastors to ensure that the spiritual and physical '
                'needs of the congregation are met.'
            ),
            'mission_statement': 'To serve Christ and His church faithfully by meeting practical needs with excellence and love.',
            'meeting_day': 'Bi-weekly',
            'meeting_time': 'After Sunday Service',
            'meeting_location': 'Church Office',
            'display_order': 6,
        },
    ]

    for item in defaults:
        slug = slugify(item['name'])
        if not Ministry.objects.filter(slug=slug).exists():
            Ministry.objects.create(
                name=item['name'],
                slug=slug,
                ministry_type=item['ministry_type'],
                short_description=item['short_description'],
                description=item['description'],
                mission_statement=item.get('mission_statement', ''),
                meeting_day=item.get('meeting_day', ''),
                meeting_time=item.get('meeting_time', ''),
                meeting_location=item.get('meeting_location', ''),
                min_age=item.get('min_age'),
                max_age=item.get('max_age'),
                is_active=True,
                is_featured=False,
                display_order=item['display_order'],
                activities='',
                requirements='',
                meta_description=item['short_description'][:160],
            )


def unseed_default_ministries(apps, schema_editor):
    Ministry = apps.get_model('ministries', 'Ministry')
    names = [
        'Pastoral Council',
        'Youth Fellowship',
        'Women Fellowship',
        'Children Ministry',
        'Singing Band',
        'Deacons Council',
    ]
    for name in names:
        Ministry.objects.filter(name=name).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ministries', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_default_ministries, unseed_default_ministries),
    ]
