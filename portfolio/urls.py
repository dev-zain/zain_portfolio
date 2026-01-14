from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-admin-now/', views.create_admin_now, name='create_admin_now'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
]