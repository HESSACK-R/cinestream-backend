# cinestream\backend\suggestions\urls.py
from rest_framework.routers import DefaultRouter
from .views import SuggestionViewSet

router = DefaultRouter()
router.register(r"suggestions", SuggestionViewSet)

urlpatterns = router.urls
