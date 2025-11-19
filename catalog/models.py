# cinestream\backend\catalog\models.py
from django.db import models

class Movie(models.Model):
    MOVIE = 'MOVIE'
    SERIES = 'SERIES'
    TYPE_CHOICES = [(MOVIE, 'Film'), (SERIES, 'Série')]

    CATEGORIES = [
        ('Action', 'Action'),
        ('Drame', 'Drame'),
        ('Comédie', 'Comédie'),
        ('Aventure', 'Aventure'),
        ('Romance', 'Romance'),
        ('Science-Fiction', 'Science-Fiction'),
        ('Horreur', 'Horreur'),
        ('Animation', 'Animation'),
    ]

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=MOVIE)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='Action')
    synopsis = models.TextField(blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    trailer_link = models.URLField(blank=True)
    price = models.PositiveIntegerField(default=0) 
    image = models.ImageField(upload_to='catalog/posters/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Season(models.Model):
    series = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons')
    number = models.PositiveIntegerField()
    episode_count = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('series', 'number')

    def __str__(self):
        return f"{self.series.title} - Saison {self.number}"
