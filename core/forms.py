"""
Forms for the core app.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form for the website."""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-teal focus:border-transparent',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-teal focus:border-transparent',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-teal focus:border-transparent',
                'placeholder': '(555) 123-4567'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-teal focus:border-transparent',
                'placeholder': 'What is this regarding?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-teal focus:border-transparent',
                'placeholder': 'Please share your message, prayer request, or question...',
                'rows': 6
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-4'),
                Column('email', css_class='form-group col-md-6 mb-4'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-4'),
                Column('subject', css_class='form-group col-md-6 mb-4'),
                css_class='form-row'
            ),
            'message',
            HTML('<div class="mt-6">'),
            Submit('submit', 'Send Message', css_class='btn-primary w-full md:w-auto'),
            HTML('</div>')
        )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common phone number formatting
            phone = ''.join(filter(str.isdigit, phone))
            if len(phone) < 10:
                raise forms.ValidationError('Please enter a valid phone number.')
        return phone
