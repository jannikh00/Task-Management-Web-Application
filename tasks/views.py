from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from .models import Profile

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
    return render(request, 'tasks/login.html', {'form': form})

# Logs out the user and redirects to login
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# Basic view for logged-in user: profile page
@login_required
def profile(request):
    return render(request, 'tasks/profile.html')