# cinestream/backend/catalog/serializers.py
from rest_framework import serializers
from .models import Movie, Season


class SeasonSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = [
            "id",
            "series",
            "number",
            "episode_count",
            "price",
            "image",
        ]

    def get_image(self, obj):
        """
        Retourne l’image de la série parente.
        (Les saisons n'ont pas d’image propre)
        """
        request = self.context.get("request")
        if not request:
            return None
        if obj.series.image and hasattr(obj.series.image, "url"):
            return request.build_absolute_uri(obj.series.image.url)
        return None


class MovieSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    seasons = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")

        if request and instance.image and hasattr(instance.image, "url"):
            rep["image"] = request.build_absolute_uri(instance.image.url)
        else:
            rep["image"] = None

        return rep

    def get_seasons(self, obj):
        """
        Retourne les saisons uniquement si l'objet est une série.
        """
        if obj.type != "SERIES":
            return []

        seasons = obj.seasons.all().order_by("number")
        return SeasonSerializer(seasons, many=True, context=self.context).data
