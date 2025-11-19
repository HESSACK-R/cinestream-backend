# cinestream\backend\suggestions\serializers.py
from rest_framework import serializers
from .models import Suggestion

class SuggestionSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()  # ✅ Nouveau champ

    class Meta:
        model = Suggestion
        fields = "__all__"

    def get_user_name(self, obj):
        """Retourne le nom complet ou le username de l'utilisateur"""
        user = obj.user
        if hasattr(user, "first_name") and user.first_name:
            return f"{user.first_name} {user.last_name}".strip()
        return user.username
