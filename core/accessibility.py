"""
Accessibility utilities for WCAG 2.1 AA compliance and enterprise-level accessibility.
"""
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import re


class AccessibilityEnhancer:
    """Utilities for improving website accessibility."""
    
    @staticmethod
    def generate_skip_links():
        """Generate skip navigation links for screen readers."""
        skip_links = [
            {'href': '#main-content', 'text': 'Skip to main content'},
            {'href': '#navigation', 'text': 'Skip to navigation'},
            {'href': '#footer', 'text': 'Skip to footer'},
        ]
        
        html = '<div class="skip-links sr-only-focusable">'
        for link in skip_links:
            html += f'<a href="{link["href"]}" class="skip-link">{link["text"]}</a>'
        html += '</div>'
        
        return mark_safe(html)
    
    @staticmethod
    def enhance_image_alt_text(alt_text, context=""):
        """Enhance image alt text for better accessibility."""
        if not alt_text:
            return "Image"
        
        # Remove redundant phrases
        redundant_phrases = [
            "image of", "picture of", "photo of", "graphic of",
            "illustration of", "screenshot of"
        ]
        
        enhanced_alt = alt_text.lower()
        for phrase in redundant_phrases:
            enhanced_alt = enhanced_alt.replace(phrase, "").strip()
        
        # Capitalize first letter
        enhanced_alt = enhanced_alt[0].upper() + enhanced_alt[1:] if enhanced_alt else "Image"
        
        # Add context if provided
        if context:
            enhanced_alt = f"{enhanced_alt} - {context}"
        
        return enhanced_alt
    
    @staticmethod
    def generate_aria_label(text, element_type="button"):
        """Generate appropriate ARIA labels for elements."""
        if element_type == "button":
            if "submit" in text.lower():
                return f"Submit {text.replace('submit', '').strip()} form"
            elif "close" in text.lower():
                return f"Close {text.replace('close', '').strip()} dialog"
            elif "menu" in text.lower():
                return f"Open {text} menu"
            else:
                return f"{text} button"
        
        elif element_type == "link":
            if "read more" in text.lower():
                return f"Read more about {text.replace('read more', '').strip()}"
            elif "download" in text.lower():
                return f"Download {text.replace('download', '').strip()}"
            else:
                return f"Navigate to {text}"
        
        return text
    
    @staticmethod
    def check_color_contrast(foreground, background):
        """
        Check color contrast ratio for accessibility compliance.
        Returns contrast ratio and compliance level.
        """
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def get_luminance(rgb):
            def normalize_color(c):
                c = c / 255.0
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            
            r, g, b = [normalize_color(c) for c in rgb]
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        fg_rgb = hex_to_rgb(foreground)
        bg_rgb = hex_to_rgb(background)
        
        fg_lum = get_luminance(fg_rgb)
        bg_lum = get_luminance(bg_rgb)
        
        # Calculate contrast ratio
        lighter = max(fg_lum, bg_lum)
        darker = min(fg_lum, bg_lum)
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)
        
        # Determine compliance level
        if contrast_ratio >= 7:
            compliance = "AAA"
        elif contrast_ratio >= 4.5:
            compliance = "AA"
        elif contrast_ratio >= 3:
            compliance = "AA Large Text"
        else:
            compliance = "Fail"
        
        return contrast_ratio, compliance
    
    @staticmethod
    def generate_structured_navigation(nav_items):
        """Generate accessible navigation structure."""
        html = '<nav role="navigation" aria-label="Main navigation">'
        html += '<ul class="nav-list" role="menubar">'
        
        for item in nav_items:
            if 'children' in item:
                html += f'''
                <li class="nav-item" role="none">
                    <a href="{item['url']}" class="nav-link" role="menuitem" 
                       aria-haspopup="true" aria-expanded="false">
                        {item['text']}
                        <span class="sr-only">(has submenu)</span>
                    </a>
                    <ul class="nav-submenu" role="menu" aria-label="{item['text']} submenu">
                '''
                for child in item['children']:
                    html += f'''
                    <li role="none">
                        <a href="{child['url']}" class="nav-sublink" role="menuitem">
                            {child['text']}
                        </a>
                    </li>
                    '''
                html += '</ul></li>'
            else:
                html += f'''
                <li class="nav-item" role="none">
                    <a href="{item['url']}" class="nav-link" role="menuitem">
                        {item['text']}
                    </a>
                </li>
                '''
        
        html += '</ul></nav>'
        return mark_safe(html)


class FormAccessibilityHelper:
    """Helper for making forms more accessible."""
    
    @staticmethod
    def enhance_form_field(field, label_text, help_text="", required=False, error_message=""):
        """Enhance form field with proper accessibility attributes."""
        field_id = f"id_{field.name}"
        
        # Generate proper label
        label_html = f'<label for="{field_id}" class="form-label'
        if required:
            label_html += ' required'
        label_html += f'">{label_text}'
        if required:
            label_html += ' <span class="required-indicator" aria-label="required">*</span>'
        label_html += '</label>'
        
        # Add accessibility attributes to field
        field_attrs = {
            'id': field_id,
            'aria-describedby': f"{field_id}_help" if help_text else None,
            'aria-required': 'true' if required else 'false',
            'aria-invalid': 'true' if error_message else 'false',
        }
        
        # Remove None values
        field_attrs = {k: v for k, v in field_attrs.items() if v is not None}
        
        # Apply attributes to field
        for attr, value in field_attrs.items():
            field.field.widget.attrs[attr] = value
        
        # Generate help text
        help_html = ""
        if help_text:
            help_html = f'<div id="{field_id}_help" class="form-help-text">{help_text}</div>'
        
        # Generate error message
        error_html = ""
        if error_message:
            error_html = f'<div id="{field_id}_error" class="form-error" role="alert">{error_message}</div>'
        
        return {
            'label_html': mark_safe(label_html),
            'field': field,
            'help_html': mark_safe(help_html),
            'error_html': mark_safe(error_html),
        }


# Template tags for accessibility
from django import template

register = template.Library()

@register.simple_tag
def accessible_image(src, alt="", context="", css_class="", width="", height=""):
    """Generate accessible image tag."""
    enhanced_alt = AccessibilityEnhancer.enhance_image_alt_text(alt, context)
    
    img_attrs = {
        'src': src,
        'alt': enhanced_alt,
        'class': css_class,
        'loading': 'lazy',
        'decoding': 'async',
    }
    
    if width:
        img_attrs['width'] = width
    if height:
        img_attrs['height'] = height
    
    # Remove empty attributes
    img_attrs = {k: v for k, v in img_attrs.items() if v}
    
    attr_string = ' '.join([f'{k}="{v}"' for k, v in img_attrs.items()])
    return format_html('<img {}>', attr_string)

@register.simple_tag
def accessible_button(text, button_type="button", css_class="", onclick="", aria_label=""):
    """Generate accessible button."""
    if not aria_label:
        aria_label = AccessibilityEnhancer.generate_aria_label(text, "button")
    
    button_attrs = {
        'type': button_type,
        'class': css_class,
        'aria-label': aria_label,
        'onclick': onclick,
    }
    
    # Remove empty attributes
    button_attrs = {k: v for k, v in button_attrs.items() if v}
    
    attr_string = ' '.join([f'{k}="{v}"' for k, v in button_attrs.items()])
    return format_html('<button {}>{}</button>', attr_string, text)

@register.simple_tag
def skip_links():
    """Generate skip navigation links."""
    return AccessibilityEnhancer.generate_skip_links()

@register.simple_tag
def screen_reader_text(text):
    """Generate screen reader only text."""
    return format_html('<span class="sr-only">{}</span>', text)
