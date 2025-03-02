from django.db import models
from django.contrib.auth.models import User

# Extending User model with Profile model
class Profile(models.Model):
    # OneToOneField to ensure each user has exactly one Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Bio as extra information on Profile
    bio = models.TextField(blank=True, default='')

    def __str__(self):
        return self.user.username