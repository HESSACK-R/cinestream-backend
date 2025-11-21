# cinestream/backend/api/urls.py
from django.urls import path, include

urlpatterns = [
    path("auth/", include("users.urls")),        
    path("users/", include("users.urls")),          
    path("orders/", include("orders.urls")),
    path("homepage/", include("homepage.urls")),
    path("suggestions/", include("suggestions.urls")),
    path("settings/", include("settings_app.urls")),
    path("catalog/", include("catalog.urls")),  
]
