# cinestream\backend\orders\admin.py
from django.contrib import admin
from .models import Order, OrderItem, Payment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "movie", "season", "price")
    list_filter = ("movie", "season")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "method", "telegram_number", "created_at")
    list_filter = ("method", "created_at")
    search_fields = ("telegram_number",)
