from django.db import migrations


def seed_leaders(apps, schema_editor):
    LeadershipProfile = apps.get_model('pages', 'LeadershipProfile')

    leaders = [
        {
            'first_name': 'Ephraim Kwaku',
            'last_name': 'Danso',
            'position': 'general_overseer',
            'specializations': 'Founder and General Overseer; Charity and Outreach Leadership',
            'display_order': 1,
            'show_on_homepage': True,
        },
        {
            'first_name': 'Theophilus',
            'last_name': 'Nsia',
            'position': 'senior_pastor',
            'display_order': 2,
        },
        {
            'first_name': 'Daniel',
            'last_name': 'Sffah',
            'position': 'senior_pastor',
            'specializations': 'Music President',
            'display_order': 3,
        },
        {
            'first_name': 'Nathaniel',
            'last_name': 'Adjei',
            'position': 'senior_pastor',
            'display_order': 4,
        },
        {
            'first_name': 'Sackey',
            'last_name': 'Unknown',
            'position': 'senior_pastor',
            'display_order': 5,
        },
        {
            'first_name': 'Yeboa',
            'last_name': 'Unknown',
            'position': 'evangelist',
            'display_order': 6,
        },
    ]

    for i, data in enumerate(leaders, start=1):
        obj, created = LeadershipProfile.objects.get_or_create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            defaults={
                'position': data.get('position', 'other'),
                'specializations': data.get('specializations', ''),
                'display_order': data.get('display_order', i),
                'is_active': True,
                'show_on_homepage': data.get('show_on_homepage', False),
            }
        )
        if not created:
            # Update core fields if already exists
            updated = False
            for field in ['position', 'specializations', 'display_order', 'show_on_homepage']:
                val = data.get(field, getattr(obj, field))
                if getattr(obj, field) != val:
                    setattr(obj, field, val)
                    updated = True
            if updated:
                obj.save()


def unseed_leaders(apps, schema_editor):
    LeadershipProfile = apps.get_model('pages', 'LeadershipProfile')
    names = [
        ('Ephraim Kwaku', 'Danso'),
        ('Theophilus', 'Nsia'),
        ('Daniel', 'Sffah'),
        ('Nathaniel', 'Adjei'),
        ('Sackey', 'Unknown'),
        ('Yeboa', 'Unknown'),
    ]
    for first, last in names:
        LeadershipProfile.objects.filter(first_name=first, last_name=last).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_seed_our_story_content'),
    ]

    operations = [
        migrations.RunPython(seed_leaders, unseed_leaders),
    ]
