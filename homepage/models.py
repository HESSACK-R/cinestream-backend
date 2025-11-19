# cinestream/backend/homepage/models.py
from django.db import models


class CarouselImage(models.Model):
    """
    🎡 Image pour le carrousel de la page d’accueil.
    Stockée dans /media/homepage/carousels/
    """
    image = models.ImageField(upload_to="homepage/carousels/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrousel #{self.id}"


class AdsImage(models.Model):
    """
    📢 Image de publicité ou d’annonce avec message optionnel.
    """
    image = models.ImageField(upload_to="homepage/ads/")
    message = models.CharField(max_length=255, blank=True, null=True)  # 🆕 message associé
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Publicité #{self.id} - {self.message or 'Sans texte'}"



class HomepageContent(models.Model):
    """
    🏠 Contenu global de la page d’accueil (textes + relations images)
    """
    welcome_text = models.CharField(
        max_length=255, default="Bienvenue sur CineStream"
    )
    top10_text = models.CharField(
        max_length=255, blank=True, default="Top 10 Afrique"
    )

    banner_images = models.ManyToManyField(CarouselImage, blank=True)
    ads_images = models.ManyToManyField(AdsImage, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Page d’accueil (maj: {self.updated_at.strftime('%Y-%m-%d %H:%M')})"
