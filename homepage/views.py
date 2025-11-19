# cinestream/backend/homepage/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import HomepageContent, CarouselImage, AdsImage
from .serializers import HomepageContentSerializer, CarouselImageSerializer, AdsImageSerializer
from orders.models import OrderItem
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os

class HomepageContentViewSet(viewsets.ModelViewSet):
    queryset = HomepageContent.objects.all()
    serializer_class = HomepageContentSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        instance.welcome_text = data.get("welcome_text", instance.welcome_text)
        instance.top10_text = data.get("top10_text", instance.top10_text)
        instance.save()

        # Ajout de nouvelles images
        for file in request.FILES.getlist("banner_images"):
            banner = CarouselImage.objects.create(image=file)
            instance.banner_images.add(banner)

        for file in request.FILES.getlist("ads_images"):
            ad = AdsImage.objects.create(image=file)
            instance.ads_images.add(ad)

        # ✅ Diffusion WebSocket (mise à jour temps réel)
        self.broadcast_homepage_update()

        serializer = HomepageContentSerializer(instance, context={"request": request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        instance = HomepageContent.objects.create(
            welcome_text=request.data.get("welcome_text", "Bienvenue sur CineStream"),
            top10_text=request.data.get("top10_text", "Top 10 Afrique")
        )

        for file in request.FILES.getlist("banner_images"):
            banner = CarouselImage.objects.create(image=file)
            instance.banner_images.add(banner)

        for file in request.FILES.getlist("ads_images"):
            ad = AdsImage.objects.create(image=file)
            instance.ads_images.add(ad)

        self.broadcast_homepage_update()
        serializer = HomepageContentSerializer(instance, context={"request": request})
        return Response(serializer.data, status=201)

    def broadcast_homepage_update(self):
        """🔔 Notifie les clients WebSocket connectés"""
        channel_layer = get_channel_layer()
        data = {"type": "homepage_update", "data": {"refresh": True}}
        async_to_sync(channel_layer.group_send)("homepage_updates", data)


class CarouselImageViewSet(viewsets.ModelViewSet):
    queryset = CarouselImage.objects.all().order_by("-id")
    serializer_class = CarouselImageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def destroy(self, request, *args, **kwargs):
        """🗑️ Supprime une image du carrousel"""
        instance = self.get_object()
        image_path = instance.image.path if instance.image else None
        instance.delete()
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        return Response({"message": "Image du carrousel supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)


class AdsImageViewSet(viewsets.ModelViewSet):
    queryset = AdsImage.objects.all().order_by("-id")
    serializer_class = AdsImageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def destroy(self, request, *args, **kwargs):
        """🗑️ Supprime une image de publicité"""
        instance = self.get_object()
        image_path = instance.image.path if instance.image else None
        instance.delete()
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        return Response({"message": "Image publicitaire supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def top10_afrique(request):
    """🔝 Retourne le Top 10 Afrique basé sur les commandes."""
    items = OrderItem.objects.select_related("movie", "season__series")
    stats = {}

    for item in items:
        if item.movie:
            title = item.movie.title
            image = item.movie.image.url if item.movie.image else ""
        elif item.season:
            title = f"{item.season.series.title} - Saison {item.season.number}"
            image = item.season.series.image.url if item.season.series.image else ""
        else:
            continue

        if title not in stats:
            stats[title] = {"title": title, "count": 0, "image": image}
        stats[title]["count"] += 1

    sorted_items = sorted(stats.values(), key=lambda x: x["count"], reverse=True)[:10]
    for item in sorted_items:
        if item["image"]:
            item["image"] = request.build_absolute_uri(item["image"])

    return Response(sorted_items)
