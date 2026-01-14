#!/usr/bin/env python
"""
Script to create superuser programmatically
Run this on Railway server using: railway run python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if admin user already exists
if User.objects.filter(username='admin').exists():
    print('Admin user already exists!')
    # Delete it to recreate
    User.objects.filter(username='admin').delete()
    print('Old admin user deleted.')

# Create new superuser
User.objects.create_superuser(
    username='devzain',
    email='your@email.com',  # Change this to your email
    password='zain35821'  # Change this to a secure password
)

print('Superuser created successfully!')
print('Username: devzain')
print('Password: zain35821')
print('IMPORTANT: Change this password after first login!')
