from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    """Model for personal profile information"""
    name = models.CharField(max_length=100, default="Zain Ali")
    title = models.CharField(max_length=200, default="Python Django Developer")
    bio = models.TextField(default="Master Student in Software Engineering at University of Hildesheim")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    email = models.EmailField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


class Skill(models.Model):
    """Model for skills"""
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50, help_text="Proficiency level (0-100)")
    category = models.CharField(max_length=50, choices=[
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ])
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-proficiency', 'name']


class Project(models.Model):
    """Model for portfolio projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(max_length=300)
    featured_image = models.ImageField(upload_to='projects/')
    
    # Technology tags
    technologies = models.CharField(max_length=300, help_text="Comma-separated technologies (e.g., Django, React, PostgreSQL)")
    
    # Project links
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    
    # Featured flag
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Order
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]
    
    class Meta:
        ordering = ['order', '-created_at']


class ProjectContent(models.Model):
    """Model for blog-style project content blocks"""
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('quote', 'Quote'),
        ('code', 'Code'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='content_blocks')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    order = models.IntegerField(default=0)
    
    # Content fields
    text_content = RichTextUploadingField(blank=True)
    image = models.ImageField(upload_to='project_content/', blank=True, null=True)
    image_caption = models.CharField(max_length=200, blank=True)
    quote_text = models.TextField(blank=True)
    quote_author = models.CharField(max_length=100, blank=True)
    code_content = models.TextField(blank=True)
    code_language = models.CharField(max_length=50, blank=True, default='python')
    
    def __str__(self):
        return f"{self.project.title} - {self.content_type} #{self.order}"
    
    class Meta:
        ordering = ['order']


class Education(models.Model):
    """Model for education history"""
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200, default="University of Hildesheim")
    field_of_study = models.CharField(max_length=200, default="Software Engineering")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Education"


class Experience(models.Model):
    """Model for work experience"""
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    class Meta:
        ordering = ['-start_date']


class ContactMessage(models.Model):
    """Model for contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']