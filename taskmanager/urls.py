"""
URL configuration for taskmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    # URL pattern for the admin site
    path('admin/', admin.site.urls),
    # URL pattern for the register site
    path('register/', views.register, name='register'),
    # URL pattern for the login site
    path('login/', views.user_login, name='login'),
    # URL pattern for logging out
    path('logout/', views.user_logout, name='logout'),
    # URL pattern for the profile page
    path('profile/', views.profile, name='profile'),
    # URL pattern for displaying the task list
    path('tasks/', views.task_list, name='task_list'),
    # URL pattern for creating a new task
    path('tasks/create/', views.task_create, name='task_create'),
    # URL pattern for updating an existing task; <int:pk> captures the task's primary key
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    # URL pattern for deleting a task; <int:pk> captures the task's primary key
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    # URL pattern for fetching task updates via AJAX
    path('ajax/task_updates/', views.ajax_task_updates, name='ajax_task_updates'),
    # URL pattern for updating a task via AJAX
    path('ajax/update_task/', views.ajax_update_task, name='ajax_update_task'),
]
