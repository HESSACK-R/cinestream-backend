# cinestream\backend\suggestions\admin.py
from django.contrib import admin
from .models import Suggestion

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("user__username", "message")
