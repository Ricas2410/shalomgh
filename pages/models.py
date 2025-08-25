"""
Models for static pages and leadership information.
"""
from django.db import models
from django.urls import reverse
from django.core.validators import EmailValidator
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os
from core.storage_backends import ImageKitStorage


class LeadershipProfile(models.Model):
    """Model for church leadership profiles."""

    POSITION_CHOICES = [
        # Senior Leadership
        ('general_overseer', 'General Overseer'),
        ('senior_pastor', 'Senior Pastor'),
        ('assistant_pastor', 'Assistant Pastor'),
        ('associate_pastor', 'Associate Pastor'),
        ('executive_pastor', 'Executive Pastor'),
        
        # Ministry Leadership
        ('worship_pastor', 'Worship Pastor'),
        ('youth_pastor', 'Youth Pastor'),
        ('children_pastor', 'Children\'s Pastor'),
        ('missions_pastor', 'Missions Pastor'),
        ('outreach_pastor', 'Outreach Pastor'),
        
        # Church Officers
        ('elder', 'Elder'),
        ('deacon', 'Deacon'),
        ('deaconess', 'Deaconess'),
        ('trustee', 'Trustee'),
        
        # Ministry Leaders
        ('minister', 'Minister'),
        ('evangelist', 'Evangelist'),
        ('teacher', 'Teacher'),
        ('prophet', 'Prophet'),
        ('apostle', 'Apostle'),
        
        # Department Heads
        ('worship_leader', 'Worship Leader'),
        ('choir_director', 'Choir Director'),
        ('sunday_school_superintendent', 'Sunday School Superintendent'),
        ('youth_leader', 'Youth Leader'),
        ('children_director', 'Children\'s Director'),
        ('women_ministry_leader', 'Women\'s Ministry Leader'),
        ('men_ministry_leader', 'Men\'s Ministry Leader'),
        
        # Administrative
        ('church_administrator', 'Church Administrator'),
        ('secretary', 'Church Secretary'),
        ('treasurer', 'Treasurer'),
        ('financial_secretary', 'Financial Secretary'),
        
        # Other
        ('missionary', 'Missionary'),
        ('chaplain', 'Chaplain'),
        ('counselor', 'Counselor'),
        ('other', 'Other'),
    ]

    # Basic Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    custom_position = models.CharField(
        max_length=100,
        blank=True,
        help_text="Use this if position is 'Other'"
    )

    # Contact Information
    email = models.EmailField(validators=[EmailValidator()], blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Profile Information
    bio = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='leadership/',
        blank=True,
        help_text="Recommended size: 400x400 pixels"
    )
    # Dedicated image for the General Overseer card (left panel on leadership page).
    # If empty, templates should fall back to `photo`.
    go_card_photo = models.ImageField(
        upload_to='leadership/go_card/',
        blank=True,
        help_text="Optional: Use a different photo for the General Overseer card"
    )

    # Ministry Information
    years_in_ministry = models.PositiveIntegerField(blank=True, null=True)
    specializations = models.TextField(
        blank=True,
        help_text="Areas of ministry specialization"
    )

    # Display Settings
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    show_on_homepage = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Leadership Profile"
        verbose_name_plural = "Leadership Profiles"
        ordering = ['display_order', 'last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} - {self.get_position_display()}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_position_display(self):
        if self.position == 'other' and self.custom_position:
            return self.custom_position
        return dict(self.POSITION_CHOICES).get(self.position, self.position)

    def get_absolute_url(self):
        return reverse('pages:leadership_detail', kwargs={'pk': self.pk})

    def get_go_card_photo(self):
        """Return the GO card image if set, else fall back to main `photo`."""
        return self.go_card_photo or self.photo

    def save(self, *args, **kwargs):
        """Save and resize the uploaded image to max 400x400.

        This implementation works with remote storage backends (e.g., ImageKit)
        by avoiding filesystem paths and operating on file-like objects.
        """
        super().save(*args, **kwargs)

        # If either photo field is empty, we still continue to check the other
        # but in ImageKit scenarios, we skip server-side resizing entirely.

        # If using ImageKitStorage, skip server-side resizing and let CDN handle transforms.
        try:
            if isinstance(getattr(self.photo, 'storage', None), ImageKitStorage):
                return
        except Exception:
            pass

        def maybe_resize(field):
            try:
                if not field:
                    return False
                field.open('rb')
                img = Image.open(field)
                img.load()
                if img.height > 400 or img.width > 400:
                    img.thumbnail((400, 400))
                    buffer = BytesIO()
                    fmt = (img.format or 'JPEG').upper()
                    save_kwargs = {'optimize': True}
                    if fmt in ('JPEG', 'JPG'):
                        save_kwargs['quality'] = 85
                    img.save(buffer, format=fmt, **save_kwargs)
                    buffer.seek(0)
                    field.save(field.name, ContentFile(buffer.read()), save=False)
                    return True
            except Exception:
                return False
            return False

        updated = False
        updated |= maybe_resize(self.photo)
        updated |= maybe_resize(self.go_card_photo)
        if updated:
            super().save(update_fields=['photo', 'go_card_photo'])


class PageContent(models.Model):
    """Model for managing static page content."""

    PAGE_CHOICES = [
        ('about', 'About Us'),
        ('our_story', 'Our Story'),
        ('beliefs', 'Our Beliefs'),
        ('mission', 'Mission Statement'),
        ('vision', 'Vision Statement'),
        ('values', 'Our Values'),
    ]

    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Meta description for SEO (max 160 characters)"
    )

    # Display Settings
    is_published = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Page Content"
        verbose_name_plural = "Page Contents"
        ordering = ['page']

    def __str__(self):
        return f"{self.get_page_display()} - {self.title}"


class WelcomeSection(models.Model):
    """Model for managing the Welcome to Our Church Family section."""

    title = models.CharField(
        max_length=200,
        default="Welcome to Our Church Family",
        help_text="Main title for the welcome section"
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        help_text="Optional subtitle below the main title"
    )
    content = models.TextField(
        help_text="Main welcome content/description"
    )

    # Image
    image = models.ImageField(
        upload_to='welcome_images/',
        blank=True,
        null=True,
        help_text="Welcome section image (recommended: 800x600px)"
    )
    image_alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alt text for the welcome image"
    )

    # Features/Highlights
    feature_1_title = models.CharField(
        max_length=100,
        default="Bible-Centered Teaching",
        help_text="First feature title"
    )
    feature_1_description = models.TextField(
        default="We believe the Bible is God's Word and the foundation for all faith and practice.",
        help_text="First feature description"
    )

    feature_2_title = models.CharField(
        max_length=100,
        default="Authentic Community",
        help_text="Second feature title"
    )
    feature_2_description = models.TextField(
        default="We foster genuine relationships where people can grow together in faith.",
        help_text="Second feature description"
    )

    feature_3_title = models.CharField(
        max_length=100,
        default="Compassionate Service",
        help_text="Third feature title"
    )
    feature_3_description = models.TextField(
        default="We serve our community and world with the love and compassion of Christ.",
        help_text="Third feature description"
    )

    # Display Settings
    is_active = models.BooleanField(
        default=True,
        help_text="Whether to display this welcome section"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Welcome Section"
        verbose_name_plural = "Welcome Sections"

    def __str__(self):
        return self.title

    @classmethod
    def get_active_welcome(cls):
        """Get the active welcome section."""
        return cls.objects.filter(is_active=True).first()
