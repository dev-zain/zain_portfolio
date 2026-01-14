from django import template
from django.conf import settings
import re

register = template.Library()

@register.filter
def cloudinary_pdf_url(cv_file):
    """Convert Cloudinary URL to proper PDF download format"""
    if not cv_file:
        return ''
    
    url = str(cv_file.url) if hasattr(cv_file, 'url') else str(cv_file)
    
    # If it's already a Cloudinary URL
    if 'cloudinary.com' in url:
        # Change resource type from 'image' to 'raw' for PDFs
        url = url.replace('/image/upload/', '/raw/upload/')
        # Add .pdf extension if missing
        if not url.endswith('.pdf'):
            url = url + '.pdf'
    
    return url
