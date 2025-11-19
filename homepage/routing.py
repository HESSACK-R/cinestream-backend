# cinestream\backend\homepage\routing.py
from django.urls import re_path
from .consumers import HomepageConsumer

websocket_urlpatterns = [
    re_path(r"ws/homepage/$", HomepageConsumer.as_asgi()),
]
