# cinestream/backend/users/views.py

from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings

from .serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


# ================================
# 🔥 TEMPORARY SUPERUSER CREATOR
# ================================
@api_view(["POST"])
@permission_classes([])   # ⛔ aucune permission (temporaire)
def create_superuser_open(request):
    """
    Route temporaire destinée uniquement au déploiement Render.
    Permet de créer un superuser même sans shell.
    Utilisation unique puis suppression.
    """

    # Sécurité minimale : interdit en local
    if settings.DEBUG:
        return Response({"error": "Indisponible en mode DEBUG"}, status=400)

    username = request.data.get("username", "admin")
    email = request.data.get("email", "admin@cinestream.com")
    password = request.data.get("password", "Admincinestream")

    if User.objects.filter(username=username).exists():
        return Response({"status": "exists", "message": "Le superuser existe déjà."})

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    return Response({
        "status": "success",
        "message": f"Superuser créé : {username}"
    })


# ======================================
# 🚀 Vues normales (non modifiées)
# ======================================

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Inscription réussie.",
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "telegram_number": user.telegram_number,
            "is_staff": user.is_staff,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
