# cinestream/backend/homepage/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import HomepageContent, CarouselImage, AdsImage
from .serializers import HomepageContentSerializer, CarouselImageSerializer, AdsImageSerializer
from orders.models import OrderItem
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class HomepageContentViewSet(viewsets.ModelViewSet):
    queryset = HomepageContent.objects.all()
    serializer_class = HomepageContentSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        # Public = lecture seule
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    # ======================================================
    # 🔥 UPDATE (PUT) — Gère parfaitement ads_messages
    # ======================================================
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # 📝 Mise à jour des textes
        instance.welcome_text = data.get("welcome_text", instance.welcome_text)
        instance.top10_text = data.get("top10_text", instance.top10_text)
        instance.save()

        # ==============================
        # 📌 Récupération des messages
        # ==============================
        ads_messages = request.data.getlist("ads_messages")

        # ==============================
        # 📌 Ajout des images carrousel
        # ==============================
        for file in request.FILES.getlist("banner_images"):
            banner = CarouselImage.objects.create(image=file)
            instance.banner_images.add(banner)

        # ==============================
        # 📌 Ajout des publicités + messages
        # ==============================
        ads_images = request.FILES.getlist("ads_images")
        for idx, file in enumerate(ads_images):
            message = ads_messages[idx] if idx < len(ads_messages) else ""
            ad = AdsImage.objects.create(image=file, message=message)
            instance.ads_images.add(ad)

        # Broadcast WebSocket
        self.broadcast_homepage_update()

        serializer = HomepageContentSerializer(instance, context={"request": request})
        return Response(serializer.data)

    # ======================================================
    # 🔥 CREATE (POST) — Gère ads_messages aussi
    # ======================================================
    def create(self, request, *args, **kwargs):
        instance = HomepageContent.objects.create(
            welcome_text=request.data.get("welcome_text", "Bienvenue sur CineStream"),
            top10_text=request.data.get("top10_text", "Top 10 Afrique")
        )

        ads_messages = request.data.getlist("ads_messages")

        # 🔹 Carrousel
        for file in request.FILES.getlist("banner_images"):
            banner = CarouselImage.objects.create(image=file)
            instance.banner_images.add(banner)

        # 🔹 Publicités + messages associés
        ads_images = request.FILES.getlist("ads_images")
        for idx, file in enumerate(ads_images):
            message = ads_messages[idx] if idx < len(ads_messages) else ""
            ad = AdsImage.objects.create(image=file, message=message)
            instance.ads_images.add(ad)

        # Broadcast WebSocket
        self.broadcast_homepage_update()

        serializer = HomepageContentSerializer(instance, context={"request": request})
        return Response(serializer.data, status=201)

    # ======================================================
    # 🔔 WebSocket Broadcast
    # ======================================================
    def broadcast_homepage_update(self):
        layer = get_channel_layer()
        data = {"type": "homepage_update", "data": {"refresh": True}}
        async_to_sync(layer.group_send)("homepage_updates", data)


# ==========================================================
# 🎡 Carrousel
# ==========================================================
class CarouselImageViewSet(viewsets.ModelViewSet):
    queryset = CarouselImage.objects.all().order_by("-id")
    serializer_class = CarouselImageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # Cloudinary → pas besoin d'os.remove
        return Response({"message": "Image carrousel supprimée."}, status=status.HTTP_204_NO_CONTENT)


# ==========================================================
# 📢 Publicités
# ==========================================================
class AdsImageViewSet(viewsets.ModelViewSet):
    queryset = AdsImage.objects.all().order_by("-id")
    serializer_class = AdsImageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Image pub supprimée."}, status=status.HTTP_204_NO_CONTENT)


# ==========================================================
# 🔝 Top 10 Afrique
# ==========================================================
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def top10_afrique(request):
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

    # Absolute URLs for frontend
    for item in sorted_items:
        if item["image"]:
            item["image"] = request.build_absolute_uri(item["image"])

    return Response(sorted_items)
