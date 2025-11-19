# cinestream/backend/orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Payment

class OrderItemSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()
    season_info = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "movie", "season", "price", "movie_title", "season_info"]

    def get_movie_title(self, obj):
        return obj.movie.title if obj.movie else None

    def get_season_info(self, obj):
        if obj.season:
            return f"{obj.season.series.title} - Saison {obj.season.number}"
        return None


class PaymentSerializer(serializers.ModelSerializer):
    screenshot = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"

    def get_screenshot(self, obj):
        request = self.context.get("request")
        if obj.screenshot and hasattr(obj.screenshot, "url"):
            return request.build_absolute_uri(obj.screenshot.url)
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_user_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.last_name}".strip() if user.first_name else user.username
