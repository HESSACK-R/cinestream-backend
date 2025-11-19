# cinestream/backend/homepage/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    HomepageContentViewSet,
    CarouselImageViewSet,
    AdsImageViewSet,
    top10_afrique,
)

router = DefaultRouter()
router.register(r"content", HomepageContentViewSet, basename="homepage-content")
router.register(r"carousels", CarouselImageViewSet, basename="carousel-images")
router.register(r"ads", AdsImageViewSet, basename="ads-images")

urlpatterns = [
    path("top10_afrique/", top10_afrique, name="top10-afrique"),
]

urlpatterns += router.urls
