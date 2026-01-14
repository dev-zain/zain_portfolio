from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Profile, Skill, Project, Education, Experience, ContactMessage
from .forms import ContactForm


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