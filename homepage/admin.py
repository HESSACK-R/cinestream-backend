# cinestream/backend/homepage/admin.py
from django.contrib import admin
from .models import HomepageContent

@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ("welcome_text", "top10_text", "updated_at")
    search_fields = ("welcome_text",)
