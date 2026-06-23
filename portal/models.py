import re
from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    ist_mitarbeiter = models.BooleanField(default=False)
    telefonnummer = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Profil von {self.user.username} ({'Mitarbeiter' if self.ist_mitarbeiter else 'Kunde'})"


class Gegenstand(models.Model):
    STATUS_CHOICES = [
        ('gefunden', 'Gefunden (im Bus abgegeben)'),
        ('gesucht', 'Verlustmeldung (vom Kunden gesucht)'),
        ('rueckgegeben', 'An Eigentümer übergeben'),
    ]

    titel = models.CharField(max_length=200)
    beschreibung = models.TextField()
    fundort = models.CharField(max_length=200)
    funddatum = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='gefunden')
    google_form_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titel} ({self.get_status_display()})"


class GegenstandBild(models.Model):
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='bilder')
    bild_url = models.URLField(max_length=500)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    @property
    def direkt_bild_url(self):
        """
        Wandelt den Google Drive Link extrem zuverlässig in ein
        direkt ladbares Vorschaubild (Thumbnail/Embed-Format) um.
        """
        url = self.bild_url.strip()

        if 'drive.google.com' in url:
            # Extrahiere die ID
            match_d = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
            match_id = re.search(r'id=([a-zA-Z0-9-_]+)', url)

            id_ = None
            if match_d:
                id_ = match_d.group(1)
            elif match_id:
                id_ = match_id.group(1)

            if id_:
                # Das 'thumbnail'-Format lädt blitzschnell und umgeht die strengen Einbettungs-Sperren von Drive
                return f"https://drive.google.com/thumbnail?sz=w600&id={id_}"

        return url

    def __str__(self):
        return f"Bild für {self.gegenstand.titel}"


class Chat(models.Model):
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='chats')
    kunde = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kunden_chats')
    mitarbeiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='mitarbeiter_chats')
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat zu {self.gegenstand.titel}"


class Nachricht(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='nachrichten')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    gesendet_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nachricht von {self.sender.username}"


class Bericht(models.Model):
    gegenstand = models.OneToOneField(Gegenstand, on_delete=models.CASCADE, related_name='bericht')
    mitarbeiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='erstellte_berichte')
    abholer_name = models.CharField(max_length=200)
    abholer_ausweis = models.CharField(max_length=100, blank=True)
    notizen = models.TextField(blank=True)
    ausgehaendigt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Übergabebericht für {self.gegenstand.titel}"