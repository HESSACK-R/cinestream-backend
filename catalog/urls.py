# cinestream/backend/catalog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeasonViewSet, catalog_dashboard

router = DefaultRouter()
router.register("movies", MovieViewSet, basename="movie")
router.register("seasons", SeasonViewSet, basename="season")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", catalog_dashboard, name="catalog-dashboard"),
]
