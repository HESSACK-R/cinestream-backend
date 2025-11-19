# cinestream/backend/settings_app/models.py
from django.db import models

class AdminSettings(models.Model):
    site_name = models.CharField(max_length=100, default="CineStream")
    description = models.TextField(blank=True, default="")
    
    # 🔶 Orange Money
    orange_money_number = models.CharField(max_length=50, blank=True)
    orange_money_name = models.CharField(max_length=100, blank=True)
    
    # 🟡 MTN Mobile Money
    mtn_money_number = models.CharField(max_length=50, blank=True)
    mtn_money_name = models.CharField(max_length=100, blank=True)

    telegram_message_default = models.TextField(
        default="Merci pour votre commande ! Notre équipe vous contactera sous peu."
    )
    homepage_about = models.TextField(blank=True, default="")
    banner_image = models.ImageField(upload_to="banners/", blank=True, null=True)

    def __str__(self):
        return "Paramètres administrateur"
