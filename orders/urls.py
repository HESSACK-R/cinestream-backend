# cinestream/backend/orders/urls.py
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"items", OrderItemViewSet, basename="order-items")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = router.urls
