from django.contrib import admin

# Registering my models here.
# This is where I'm importing the Check_In
from .models import Check_In

# Registering the model here so the admin site can pick it up
admin.site.register(Check_In)
