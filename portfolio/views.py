from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Profile, Skill, Project, Education, Experience, ContactMessage
from .forms import ContactForm


def create_admin_now(request):
    """Emergency admin creation - uses environment variables"""
    from django.http import HttpResponse
    from django.contrib.auth import get_user_model
    from decouple import config
    User = get_user_model()
    
    try:
        username = config('ADMIN_USERNAME', default='admin')
        password = config('ADMIN_PASSWORD', default='changeme123')
        email = config('ADMIN_EMAIL', default='admin@example.com')
        
        # Delete existing user if exists
        User.objects.filter(username=username).delete()
        # Create new one
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse(f'<h1 style="color:green;">✅ Admin Created!</h1><p>Username: {username}</p><p><a href="/admin/">Login Now</a></p><p style="color:red;">Password is from ADMIN_PASSWORD env var</p>')
    except Exception as e:
        return HttpResponse(f'<h1 style="color:red;">Error: {e}</h1>')


def index(request):
    """Homepage view"""
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    education = Education.objects.all()
    experience = Experience.objects.all()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    # Handle contact form
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('index')
    else:
        form = ContactForm()
    
    context = {
        'profile': profile,
        'skills_by_category': skills_by_category,
        'featured_projects': featured_projects,
        'education': education,
        'experience': experience,
        'form': form,
    }
    return render(request, 'index.html', context)


def projects(request):
    """Projects listing view"""
    all_projects = Project.objects.all()
    
    context = {
        'projects': all_projects,
    }
    return render(request, 'projects.html', context)


def project_detail(request, slug):
    """Individual project detail view"""
    project = get_object_or_404(Project, slug=slug)
    content_blocks = project.content_blocks.all()
    
    context = {
        'project': project,
        'content_blocks': content_blocks,
    }
    return render(request, 'project_detail.html', context)