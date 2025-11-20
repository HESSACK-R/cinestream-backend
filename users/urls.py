# cinestream/backend/users/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    CustomLoginView,
    UserViewSet,
    create_superuser_open
)

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 🚨 TEMPORAIRE — CRÉATION SUPERUSER
    path("create-superuser/", create_superuser_open, name="create_superuser"),
]

urlpatterns += router.urls
