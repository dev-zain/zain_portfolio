from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setup-admin/', views.setup_admin, name='setup_admin'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
]