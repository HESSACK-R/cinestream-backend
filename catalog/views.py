# cinestream\backend\catalog\views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count
from .models import Movie, Season
from orders.models import Payment, Order
from .serializers import MovieSerializer, SeasonSerializer

@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def catalog_dashboard(request):
    """
    📊 Tableau de bord administratif complet :
    - Totaux (films, séries, saisons)
    - Valeur totale du catalogue
    - Nouveaux ajouts récents
    - Revenus hebdomadaires réels
    - Dernières sorties
    """
    now = timezone.now()
    last_week = now - timedelta(days=7)

    # 🧮 Totaux
    total_movies = Movie.objects.filter(type="MOVIE").count()
    total_series = Movie.objects.filter(type="SERIES").count()
    total_seasons = Season.objects.count()

    # 💰 Valeur totale du catalogue
    total_movie_price = Movie.objects.aggregate(total=Sum("price"))["total"] or 0
    total_season_price = Season.objects.aggregate(total=Sum("price"))["total"] or 0
    total_price = total_movie_price + total_season_price

    # 🆕 Nouveaux ajouts cette semaine
    new_movies = Movie.objects.filter(created_at__gte=last_week).count()
    new_seasons = Season.objects.filter(series__created_at__gte=last_week).count()

    # 🎞 Derniers contenus ajoutés
    latest_movies = list(
        Movie.objects.order_by("-created_at").values("id", "title", "price", "image", "created_at", "type")[:5]
    )
    latest_seasons = list(
        Season.objects.select_related("series").order_by("-id").values(
            "id", "price", "number", "series__title"
        )[:5]
    )

    latest_content = [
        {
            "id": s["id"],
            "title": f"{s['series__title']} - Saison {s['number']}",
            "price": s["price"],
            "type": "SAISON",
            "image": None,
        }
        for s in latest_seasons
    ] + [
        {
            "id": m["id"],
            "title": m["title"],
            "price": m["price"],
            "type": m["type"],
            "image": m["image"],
        }
        for m in latest_movies
    ]

    latest_content = sorted(latest_content, key=lambda x: x["id"], reverse=True)[:5]

    # 💸 Revenus des 7 derniers jours
    today = now.date()
    start_date = today - timedelta(days=6)
    payments = Payment.objects.filter(created_at__date__gte=start_date)

    daily_data = (
        payments.values("created_at__date")
        .annotate(total=Sum("order__total_price"))
        .order_by("created_at__date")
    )

    revenue_trend = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        total_day = next(
            (d["total"] for d in daily_data if d["created_at__date"] == day), 0
        )
        revenue_trend.append({
            "date": day.strftime("%a"),
            "total": total_day,
        })

    # 📦 Commandes par jour (pour future courbe multi-lignes)
    order_data = (
        Order.objects.filter(created_at__date__gte=start_date)
        .values("created_at__date")
        .annotate(count=Count("id"))
        .order_by("created_at__date")
    )

    orders_trend = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        count_day = next(
            (d["count"] for d in order_data if d["created_at__date"] == day), 0
        )
        orders_trend.append({
            "date": day.strftime("%a"),
            "count": count_day,
        })

    data = {
        "total_movies": total_movies,
        "total_series": total_series,
        "total_seasons": total_seasons,
        "total_price": total_price,
        "new_movies_this_week": new_movies,
        "new_seasons_this_week": new_seasons,
        "latest_content": latest_content,
        "revenue_trend": revenue_trend,
        "orders_trend": orders_trend,
    }

    return Response(data)

# === CRUD existants ===
class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Movie.objects.all().order_by("-created_at")
        movie_type = self.request.query_params.get("type")
        category = self.request.query_params.get("category")

        if movie_type in ["MOVIE", "SERIES"]:
            queryset = queryset.filter(type=movie_type)
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class SeasonViewSet(viewsets.ModelViewSet):
    serializer_class = SeasonSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Season.objects.all().order_by("number")
        series_id = self.request.query_params.get("series")
        if series_id:
            queryset = queryset.filter(series_id=series_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
