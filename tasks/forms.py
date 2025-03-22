from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Task

# User Creation Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class TaskForm(forms.ModelForm):
    # This ModelForm automatically creates form fields based on the Task model fields
    class Meta:
        # Specify that this form is for the Task model
        model = Task
        # Define the fields to include in the form
        fields = ['title', 'description', 'due_date', 'status', 'assigned_to']