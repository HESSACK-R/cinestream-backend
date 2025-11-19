# cinestream\backend\catalog\admin.py
from django.contrib import admin
from .models import Movie, Season

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "release_year")
    list_filter = ("type", "release_year")
    search_fields = ("title",)

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("series", "number", "episode_count", "price")
    list_filter = ("series",)
