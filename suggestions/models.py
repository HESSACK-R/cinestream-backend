# cinestream\backend\suggestions\models.py
from django.db import models
from django.conf import settings
from telegram_bot.bot import notify_admin
from datetime import datetime
from django.db.models.signals import post_save

class Suggestion(models.Model):
    CATEGORY_CHOICES = [
        ("BUG", "Bug ou problème"),
        ("IDEA", "Idée d’amélioration"),
        ("COMMENT", "Commentaire général"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="suggestions"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("PENDING", "En attente"), ("RESOLVED", "Résolu")],
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}"

def send_suggestion_notification(sender, instance, created, **kwargs):
    if created:
        message = (
            "💡 *Nouvelle suggestion reçue !*\n\n"
            f"👤 Utilisateur : *{instance.user.username}*\n"
            f"📂 Catégorie : *{instance.get_category_display()}*\n"
            f"🕒 Date : {instance.created_at.strftime('%d/%m/%Y %H:%M')}\n"
            f"💬 Message : {instance.message}\n\n"
            "🔗 Consultez-la dans l’espace admin : /admin/suggestions/suggestion/"
        )
        notify_admin(message)

post_save.connect(send_suggestion_notification, sender=Suggestion)