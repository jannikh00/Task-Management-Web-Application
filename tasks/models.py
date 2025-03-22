from django.db import models
from django.contrib.auth.models import User

# Extending User model with Profile model
class Profile(models.Model):
    # OneToOneField to ensure each user has exactly one Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Bio as extra information on Profile, can be left empty
    bio = models.TextField(blank=True, default='')

    def __str__(self):
        return self.user.username
    
class Task(models.Model):
    # Field for the task's title with a maximum length of 200 characters
    title = models.CharField(max_length=200)       

    # Field for a detailed description of the task; can be left empty
    description = models.TextField(blank=True)       

    # Field for the task's due date; can be null or left blank
    due_date = models.DateField(null=True, blank=True)  

    # Boolean field to represent task status; False = not completed, True = completed
    status = models.BooleanField(default=False)       

    # ForeignKey to assign the task to a User; if the user is deleted, this field is set to NULL
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  

    # Automatically records the timestamp when a task is created
    created_at = models.DateTimeField(auto_now_add=True)  

    # Automatically updates the timestamp whenever a task is modified
    updated_at = models.DateTimeField(auto_now=True)      

    # String representation of the Task, returning its title
    def __str__(self):
        return self.title