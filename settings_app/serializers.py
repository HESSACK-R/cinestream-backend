# cinestream/backend/settings_app/serializers.py
from rest_framework import serializers
from .models import AdminSettings

class AdminSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSettings
        fields = "__all__"
