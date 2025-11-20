# cinestream/backend/users/views.py

from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


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
