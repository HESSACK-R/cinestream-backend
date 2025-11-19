# cinestream\backend\users\urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .views import RegisterView, CustomLoginView, UserViewSet

# --- Router REST pour les utilisateurs ---
router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls


# ============================================================
# 🚨 ROUTE TEMPORAIRE : CRÉATION AUTO D’UN SUPERUSER SUR RENDER
# ============================================================
def create_superuser(request):
    """
    Cette route crée un superuser *une seule fois*.
    À visiter seulement une fois :
        /api/users/create-superuser/
    Puis SUPPRIMER ce bloc.
    """

    User = get_user_model()

    # Vérifie si déjà créé
    if User.objects.filter(username="admin").exists():
        return JsonResponse({"status": "exists", "message": "Le superuser existe déjà."})

    # Création
    User.objects.create_superuser(
        username="admin",
        password="Admincinestream",
        email="admin@cinestream.com"
    )

    return JsonResponse({
        "status": "success",
        "message": "Superuser créé : admin / Admin123!"
    })


# 👉 Route d'exécution (à supprimer après utilisation)
urlpatterns += [
    path("create-superuser/", create_superuser),
]
