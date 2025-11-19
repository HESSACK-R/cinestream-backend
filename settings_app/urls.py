# cinestream/backend/settings_app/urls.py
from rest_framework.routers import DefaultRouter
from .views import AdminSettingsViewSet

router = DefaultRouter()
router.register(r"settings", AdminSettingsViewSet)

urlpatterns = router.urls
