from django.db import models
from django.contrib.auth.models import User


# Erweiterung für das Benutzerprofil, um die Rollen sauber zu trennen
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('kunde', 'Kunde (Suchender)'),
        ('mitarbeiter', 'Mitarbeiter (Fundbüro-Bearbeiter)'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rolle = models.CharField(max_length=20, choices=ROLE_CHOICES, default='kunde')
    telefonnummer = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_rolle_display()})"


# Das Modell für die Fundgegenstände (wird später mit den CSV-Daten abgeglichen)
class Gegenstand(models.Model):
    STATUS_CHOICES = [
        ('verfuegbar', 'Verfügbar / Offen'),
        ('bearbeitung', 'In Bearbeitung / Chat aktiv'),
        ('ausgehaendigt', 'Ausgehändigt / Abgeschlossen'),
    ]

    google_form_id = models.CharField(max_length=100, unique=True, verbose_name="Zeitstempel/ID von Google")
    titel = models.CharField(max_length=200, verbose_name="Gegenstand")
    beschreibung = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    fundort = models.CharField(max_length=200, blank=True, null=True, verbose_name="Fundort")
    funddatum = models.CharField(max_length=100, blank=True, null=True, verbose_name="Funddatum")
    bild_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Bild-Link (Google Drive)")

    # Der aktuelle Status steuert, ob der Gegenstand öffentlich sichtbar ist
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='verfuegbar')
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titel} [{self.get_status_display()}]"


# Ein privater Chatraum pro Gegenstand und Kunde
class ChatRoom(models.Model):
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='chats')
    kunde = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kunde_chats')
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('gegenstand', 'kunde')  # Pro Kunde und Gegenstand nur ein Chatraum

    def __str__(self):
        return f"Chat: {self.kunde.username} zu {self.gegenstand.titel}"


# Die einzelnen Chat-Nachrichten im Raum
class ChatMessage(models.Model):
    raum = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='nachrichten')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    nachricht = models.TextField()
    gesendet_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Von {self.sender.username} am {self.gesendet_am.strftime('%d.%m.%Y %H:%M')}"


# Der rechtlich bindende Übergabebericht zum Ausdrucken
class UebergabeBericht(models.Model):
    gegenstand = models.OneToOneField(Gegenstand, on_delete=models.CASCADE, related_name='bericht')
    kunde = models.ForeignKey(User, on_delete=models.PROTECT, related_name='berichte_empfangen',
                              verbose_name="Abholer (Kunde)")
    bearbeiter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='berichte_erstellt',
                                   verbose_name="Mitarbeiter")
    uebergabe_datum = models.DateTimeField(auto_now_add=True, verbose_name="Zeitpunkt der Übergabe")
    bemerkung = models.TextField(blank=True, null=True, verbose_name="Interne Vermerke (z.B. Ausweisnummer)")

    def __str__(self):
        return f"Bericht für {self.gegenstand.titel} - {self.uebergabe_datum.strftime('%d.%m.%Y')}"