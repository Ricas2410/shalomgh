from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20250801_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='map_query',
            field=models.CharField(
                blank=True,
                help_text="Address or GPS coordinates for Google Maps (e.g., '5.6037,-0.1870' or '123 Church St, Accra')",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='map_embed_url',
            field=models.URLField(
                blank=True,
                help_text='Optional full Google Maps embed URL. If blank, an embed will be generated from map_query/address when possible.'
            ),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='directions_heading',
            field=models.CharField(
                blank=True,
                default='Directions',
                help_text='Heading label for the directions section',
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='directions_details',
            field=models.TextField(
                blank=True,
                help_text='Optional rich text/HTML with step-by-step directions or landmarks',
            ),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='directions_link_text',
            field=models.CharField(
                blank=True,
                default='Get Directions',
                help_text='CTA text for the directions button',
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='directions_link_url',
            field=models.URLField(
                blank=True,
                help_text='Optional custom URL for the directions button. If blank, a Google Maps link will be generated from map_query/address.'
            ),
        ),
    ]
