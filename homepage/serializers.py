# cinestream/backend/homepage/serializers.py
from rest_framework import serializers
from .models import HomepageContent, CarouselImage, AdsImage


class CarouselImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CarouselImage
        fields = ["id", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class AdsImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = AdsImage
        fields = ["id", "image", "message"]

    def get_image(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class HomepageContentSerializer(serializers.ModelSerializer):
    banner_images = CarouselImageSerializer(many=True, read_only=True)
    ads_images = AdsImageSerializer(many=True, read_only=True)

    class Meta:
        model = HomepageContent
        fields = "__all__"
