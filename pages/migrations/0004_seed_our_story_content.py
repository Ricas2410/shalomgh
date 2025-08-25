from django.db import migrations


def seed_our_story_content(apps, schema_editor):
    PageContent = apps.get_model('pages', 'PageContent')

    # Only create if it doesn't already exist
    if not PageContent.objects.filter(page='our_story').exists():
        PageContent.objects.create(
            page='our_story',
            title='Our Story',
            content=(
                """
                Our church began as a small gathering of families united by a desire to worship in spirit and truth,
                live out the Sabbath faithfully, and share the love of Christ with our community. By God’s grace,
                what started humbly has grown into a vibrant church family committed to Scripture, discipleship,
                and compassionate service.

                Over the years, the Lord has guided us through seasons of growth, outreach, and missions. We’ve
                seen lives transformed, leaders raised, and new ministries launched to meet the spiritual and
                practical needs of people around us. Today, we remain steadfast in our calling—to proclaim the
                Gospel, nurture believers, and serve our neighbors with the heart of Christ.

                As we look ahead, we trust God for greater impact: strengthening families, equipping the next
                generation, and advancing the Kingdom through worship, teaching, and acts of love.
                """
            ).strip(),
            meta_description=(
                "Discover the history and journey of our church—how God has been faithful from our founding to today."
            ),
            is_published=True,
        )


def unseed_our_story_content(apps, schema_editor):
    PageContent = apps.get_model('pages', 'PageContent')
    # Be conservative: only delete the record if it's the only one for our_story
    qs = PageContent.objects.filter(page='our_story')
    if qs.count() == 1:
        qs.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_leadershipprofile_position'),
    ]

    operations = [
        migrations.RunPython(seed_our_story_content, unseed_our_story_content),
    ]
