# cinestream\backend\users\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomLoginView, UserViewSet

# --- Router REST pour les utilisateurs ---
router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# ✅ Ajoute la route de l'API /api/auth/users/
urlpatterns += router.urls