from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, TaskForm
from .models import Profile, Task
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse


# User sign-up, creates a user and an empty profile
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Creates the User
            Profile.objects.create(user=user)  # Create a blank Profile automatically
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    # Render the register template
    return render(request, 'tasks/register.html', {'form': form})

# Uses Django's AuthenticationForm for the login process
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    # Render the login template
    return render(request, 'tasks/login.html', {'form': form})

# Logs out the user and redirects to login
# Ensures only logged-in users can access this view
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# Basic view for logged-in user: profile page
@login_required
def profile(request):
    # Render the profile template
    return render(request, 'tasks/profile.html')

# View to display all tasks
@login_required
def task_list(request):
    # Retrieve all Task objects from the database
    tasks = Task.objects.all()
    # Render template with tasks
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# View to create a new task
@login_required
def task_create(request):
    # Check if the form was submitted via POST
    if request.method == 'POST':
        # Create a TaskForm with the submitted data
        form = TaskForm(request.POST)
        # Validate the form data
        if form.is_valid():
            # Save the new task to the database
            form.save()
            # Redirect to the task list after saving
            return redirect('task_list')
    else:
        # For a GET request, create an empty TaskForm
        form = TaskForm()
    # Render the form template
    return render(request, 'tasks/task_form.html', {'form': form})

# View to update an existing task
@login_required
def task_update(request, pk):
    # Retrieve the task by primary key or return 404 if not found
    task = get_object_or_404(Task, pk=pk)
    # If the form is submitted
    if request.method == 'POST':
        # Bind the submitted data to the existing task instance
        form = TaskForm(request.POST, instance=task)
        # Validate the form data
        if form.is_valid():
            # Save the updated task
            form.save()
            # Redirect to the task list after saving
            return redirect('task_list')
    else:
        # For a GET request, pre-populate the form with the task's current data
        form = TaskForm(instance=task)
    # Render the form template
    return render(request, 'tasks/task_form.html', {'form': form})

# View to delete an existing task
@login_required
def task_delete(request, pk):
    # Retrieve the task by primary key or return 404 if not found
    task = get_object_or_404(Task, pk=pk)
    # Check if the deletion is confirmed via POST
    if request.method == 'POST':
        # Delete the task from the database
        task.delete()
        # Redirect to the task list after deletion
        return redirect('task_list')
    # Render a confirmation template
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

# View to fetch task updates
@require_GET  # Allow only GET requests for fetching tasks
def ajax_task_updates(request):
    tasks = list(Task.objects.values())  # Retrieve all tasks and convert QuerySet to list
    return JsonResponse({'tasks': tasks})  # Return tasks as a JSON response

# View to update task status
@require_POST  # Allow only POST requests for updating tasks
def ajax_update_task(request):
    import json  # Import json module to parse JSON data
    data = json.loads(request.body)  # Parse JSON data from the request body
    task_id = data.get('id')  # Extract task ID from the data
    status = data.get('status')  # Extract new status from the data
    try:
        task = Task.objects.get(id=task_id)  # Retrieve the task by its ID
        task.status = status  # Update the task status
        task.save()  # Save changes to the database
        # Notify WebSocket clients about the update
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "tasks_group",  # Send to the tasks group
            {
                'type': 'task_update',  # Custom event type for task updates
                'message': {'id': task_id, 'status': status}  # Include update details
            }
        )
        return JsonResponse({'success': True})  # Return success response
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)  # Return error if task not found