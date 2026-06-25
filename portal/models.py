from django.db import models
from django.contrib.auth.models import User

class Gegenstand(models.Model):
    STATUS_CHOICES = [
        ('gefunden', 'Gefunden (im Bus abgegeben)'),
        ('rueckgegeben', 'An Eigentümer übergeben'),
    ]

    titel = models.CharField(max_length=200)
    beschreibung = models.TextField()
    fundort = models.CharField(max_length=200)  # z.B. "Linie Stadtbus 3 (Bus: BD-14742)"
    funddatum = models.CharField(max_length=100) # Flexibel als String aus Google Forms
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='gefunden')

    def __str__(self):
        return self.titel

class GegenstandBild(models.Model):
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='bilder')
    bild_url = models.URLField(max_length=500)       # Link zur Großansicht
    direkt_bild_url = models.URLField(max_length=500) # Link für das <img>-Tag

    def __str__(self):
        return f"Bild für {self.gegenstand.titel}"

class Nachricht(models.Model):
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='nachrichten')
    absender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    zeitstempel = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['zeitstempel'] # Älteste Nachrichten zuerst

    def __str__(self):
        return f"Nachricht von {self.absender.username} zu {self.gegenstand.titel}"