# cinestream/backend/users/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, CustomLoginView

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", CustomLoginView.as_view(), name="login"),
]

urlpatterns += router.urls
