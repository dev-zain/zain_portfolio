from django.contrib import admin
from django import forms
from django.db import models  # ← ADD THIS LINE
from django.utils.html import format_html
from .models import Profile, Skill, Project, ProjectContent, Education, Experience, ContactMessage
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProjectContentInlineForm(forms.ModelForm):
    """Custom form for ProjectContent with proper CKEditor widget"""
    text_content = forms.CharField(
        widget=CKEditorUploadingWidget(),
        required=False,
        label='Text Content'
    )
    
    class Meta:
        model = ProjectContent
        fields = '__all__'


class ProjectContentInline(admin.StackedInline):
    """Stacked inline for better layout with CKEditor"""
    model = ProjectContent
    form = ProjectContentInlineForm
    extra = 1
    fields = [
        'content_type', 
        'order', 
        'text_content', 
        'image', 
        'image_caption', 
        'quote_text', 
        'quote_author', 
        'code_content', 
        'code_language'
    ]
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'title', 'bio', 'profile_image')
        }),
        ('Contact Information', {
            'fields': ('email', 'github', 'linkedin', 'twitter')
        }),
        ('Documents', {
            'fields': ('cv',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one profile
        if Profile.objects.exists():
            return False
        return True


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency']
    list_filter = ['category']
    search_fields = ['name']
    list_editable = ['proficiency']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'order', 'content_count', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectContentInline]
    list_editable = ['is_featured', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'featured_image'),
            'description': 'Main project information'
        }),
        ('Technical Details', {
            'fields': ('technologies',),
            'description': 'Comma-separated technologies (e.g., Django, React, PostgreSQL)'
        }),
        ('Links', {
            'fields': ('github_url', 'live_url'),
            'description': 'Project URLs'
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order'),
            'description': 'Lower order numbers appear first'
        }),
    )
    
    def content_count(self, obj):
        """Show number of content blocks"""
        count = obj.content_blocks.count()
        if count == 0:
            return format_html('<span style="color: #999;">No content</span>')
        return format_html('<span style="color: #417690; font-weight: bold;">{} blocks</span>', count)
    content_count.short_description = 'Content Blocks'


@admin.register(ProjectContent)
class ProjectContentAdmin(admin.ModelAdmin):
    list_display = ['get_project_title', 'content_type', 'order', 'preview', 'created_date']
    list_filter = ['content_type', 'project']
    list_editable = ['order']
    search_fields = ['project__title', 'text_content', 'quote_text']
    ordering = ['project', 'order']
    
    fieldsets = (
        ('Basic', {
            'fields': ('project', 'content_type', 'order'),
            'description': 'Select project and content type'
        }),
        ('Text Content', {
            'fields': ('text_content',),
            'classes': ('collapse',),
            'description': 'For "text" content type'
        }),
        ('Image Content', {
            'fields': ('image', 'image_caption'),
            'classes': ('collapse',),
            'description': 'For "image" content type'
        }),
        ('Quote Content', {
            'fields': ('quote_text', 'quote_author'),
            'classes': ('collapse',),
            'description': 'For "quote" content type'
        }),
        ('Code Content', {
            'fields': ('code_content', 'code_language'),
            'classes': ('collapse',),
            'description': 'For "code" content type'
        }),
    )
    
    def get_project_title(self, obj):
        """Show project title with link"""
        return format_html(
            '<a href="/admin/portfolio/project/{}/change/" style="font-weight: bold; color: #417690;">{}</a>',
            obj.project.id,
            obj.project.title
        )
    get_project_title.short_description = 'Project'
    get_project_title.admin_order_field = 'project__title'
    
    def preview(self, obj):
        """Show content preview"""
        if obj.content_type == 'text':
            # Strip HTML tags and truncate
            import re
            text = re.sub('<[^<]+?>', '', obj.text_content or '')
            return text[:100] + '...' if len(text) > 100 else text
        elif obj.content_type == 'image':
            if obj.image:
                return format_html('<img src="{}" style="max-height: 50px; max-width: 100px; border-radius: 4px;" />', obj.image.url)
            return obj.image_caption or 'No image'
        elif obj.content_type == 'quote':
            text = obj.quote_text or ''
            return f'"{text[:80]}..."' if len(text) > 80 else f'"{text}"'
        elif obj.content_type == 'code':
            return f'{obj.code_language or "Code"}'
        return '-'
    preview.short_description = 'Preview'
    
    def created_date(self, obj):
        """Show when it was created"""
        return obj.project.created_at.strftime('%Y-%m-%d')
    created_date.short_description = 'Date'
    created_date.admin_order_field = 'project__created_at'
    
    # Add actions for bulk operations
    actions = ['duplicate_content', 'move_to_top', 'move_to_bottom']
    
    def duplicate_content(self, request, queryset):
        """Duplicate selected content blocks"""
        count = 0
        for content in queryset:
            content.pk = None
            content.order = content.project.content_blocks.count()
            content.save()
            count += 1
        self.message_user(request, f'{count} content block(s) duplicated.')
    duplicate_content.short_description = 'Duplicate selected content'
    
    def move_to_top(self, request, queryset):
        """Move selected content to top"""
        for content in queryset:
            content.order = -1
            content.save()
        self.message_user(request, 'Moved to top.')
    move_to_top.short_description = 'Move to top'
    
    def move_to_bottom(self, request, queryset):
        """Move selected content to bottom"""
        for content in queryset:
            max_order = content.project.content_blocks.aggregate(models.Max('order'))['order__max'] or 0
            content.order = max_order + 1
            content.save()
        self.message_user(request, 'Moved to bottom.')
    move_to_bottom.short_description = 'Move to bottom'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    list_editable = ['is_current']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    list_editable = ['is_current']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['is_read']
    
    def has_add_permission(self, request):
        return False