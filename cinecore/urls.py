# cinestream\backend\cinecore\urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("api/users/", include("users.urls")),
    path("api/catalog/", include("catalog.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/homepage/", include("homepage.urls")),
    path("api/suggestions/", include("suggestions.urls")),
    path("api/settings/", include("settings_app.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)