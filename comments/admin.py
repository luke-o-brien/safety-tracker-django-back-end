from django.contrib import admin

# Registering models
from .models import Comment

admin.site.register(Comment)
