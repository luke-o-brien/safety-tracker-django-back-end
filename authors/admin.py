from django.contrib import admin

# Registering the author model
from .models import Author

admin.site.register(Author)
