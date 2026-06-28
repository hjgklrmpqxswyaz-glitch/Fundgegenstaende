from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Gegenstand(models.Model):
    STATUS_CHOICES = [
        ('verfuegbar', 'Verfügbar / Wartet auf Abholung'),
        ('rueckgegeben', 'An Kunden übergeben / Archiviert'),
        ('entsorgt', 'Nach Fristablauf entsorgt / Archiviert'),
    ]

    bezeichnung = models.CharField(max_length=200, verbose_name="Bezeichnung")
    fundort = models.CharField(max_length=200, verbose_name="Bus-Linie / Fundort")
    funddatum = models.DateField(verbose_name="Funddatum")
    funduhrzeit = models.TimeField(null=True, blank=True, verbose_name="Funduhrzeit")
    beschreibung = models.TextField(verbose_name="Aktueller Verbleib / Beschreibung")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='verfuegbar', verbose_name="Status")
    erstellt_am = models.DateTimeField(default=timezone.now, verbose_name="System-Eintragsdatum")
    rohe_bild_urls = models.TextField(blank=True, null=True, verbose_name="Rohe Bild-URLs vom Formular")

    unterschriebener_beleg = models.FileField(
        upload_to='uebergabebelege/',
        null=True,
        blank=True,
        verbose_name="Gescannter Übergabeschein (PDF/Bild)"
    )

    class Meta:
        verbose_name = "Fundgegenstand"
        verbose_name_plural = "Fundgegenstände"
        ordering = ['-funddatum', '-funduhrzeit']

    def __str__(self):
        return f"{self.bezeichnung} ({self.fundort}) - {self.get_status_display()}"

    def ist_abgelaufen(self):
        if self.funddatum:
            zeitspanne = timezone.now().date() - self.funddatum
            return zeitspanne.days > 365
        return False


class GegenstandBild(models.Model):
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='bilder')
    bild_url = models.URLField(max_length=500, verbose_name="Original Bild URL (Google Drive)")
    direkt_bild_url = models.URLField(max_length=500, blank=True, default='', verbose_name="Direkt-Lade Bild URL")

    class Meta:
        verbose_name = "Gegenstand Bild"
        verbose_name_plural = "Gegenstand Bilder"


class TicketNachricht(models.Model):
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='nachrichten')
    kunde = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kunde_tickets')
    absender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gesendete_nachrichten')
    inhalt = models.TextField(verbose_name="Nachrichtentext")
    gesendet_am = models.DateTimeField(auto_now_add=True, verbose_name="Sendezeitpunkt")

    class Meta:
        verbose_name = "Ticket-Nachricht"
        verbose_name_plural = "Ticket-Nachrichten"
        ordering = ['gesendet_am']

    def __str__(self):
        return f"Chat zu {self.gegenstand.bezeichnung} - Von: {self.absender.username}"