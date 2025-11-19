# cinestream/backend/settings_app/views.py
from rest_framework import viewsets, permissions
from .models import AdminSettings
from .serializers import AdminSettingsSerializer

class AdminSettingsViewSet(viewsets.ModelViewSet):
    queryset = AdminSettings.objects.all()
    serializer_class = AdminSettingsSerializer

    def get_permissions(self):
        """Permet à tout le monde de lire, mais limite l'édition aux admins."""
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]  # ✅ public
        else:
            permission_classes = [permissions.IsAdminUser]  # 🔒 admin only
        return [permission() for permission in permission_classes]
