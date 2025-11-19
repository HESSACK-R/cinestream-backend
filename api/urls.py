# cinestream\backend\api\urls.py
from django.urls import path, include

urlpatterns = [
    path("auth/", include("users.urls")),
    path("catalog/", include("catalog.urls")),
    path("orders/", include("orders.urls")),
    path("homepage/", include("homepage.urls")),
    path("suggestions/", include("suggestions.urls")),
]
