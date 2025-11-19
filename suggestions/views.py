# cinestream\backend\suggestions\views.py
from rest_framework import viewsets, permissions
from .models import Suggestion
from .serializers import SuggestionSerializer

class SuggestionViewSet(viewsets.ModelViewSet):
    queryset = Suggestion.objects.all().order_by("-created_at")
    serializer_class = SuggestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Suggestion.objects.all().order_by("-created_at")
        return Suggestion.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
