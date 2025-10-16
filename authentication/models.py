from django.db import models
from django.contrib.auth.models import AbstractUser #This is the user model that already exists in django.

# Extending the AbstractUser and adding the fields that I want for my users
class User(AbstractUser): 
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=300)

