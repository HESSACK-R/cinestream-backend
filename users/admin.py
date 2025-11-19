# cinestream\backend\users\admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "telegram_number", "is_staff", "is_active")
    search_fields = ("username", "email", "telegram_number")
