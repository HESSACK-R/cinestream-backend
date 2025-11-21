# cinestream\backend\orders\models.py
from django.db import models
from django.conf import settings
from users.models import User
from catalog.models import Movie, Season

class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "En attente"),
        ("PAID", "Payé"),       
        ("DELIVERED", "Livré"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Article {self.id} ({self.order})"


class Payment(models.Model):
    METHOD_CHOICES = [
        ("OM", "Orange Money"),
        ("MOMO", "MTN MoMo"),
    ]

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    method = models.CharField(max_length=5, choices=METHOD_CHOICES)
    screenshot = models.ImageField(upload_to="payments/")
    telegram_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.id} ({self.method})"

