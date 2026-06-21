from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    ist_mitarbeiter = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({'Mitarbeiter' if self.ist_mitarbeiter else 'Kunde'})"

class Gegenstand(models.Model):
    STATUS_CHOICES = [
        ('gesucht', 'Gesucht (vom Kunden gemeldet)'),
        ('gefunden', 'Gefunden (im Bus abgegeben)'),
        ('rueckgegeben', 'An Eigentümer übergeben'),
    ]

    google_form_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField(blank=True)
    fundort = models.CharField(max_length=200, blank=True)
    funddatum = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='gefunden')
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titel

class GegenstandBild(models.Model):
    # Verknüpfung: Ein Gegenstand kann mehrere Bilder haben
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='bilder')
    bild_url = models.URLField(max_length=1000)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gegenstand-Bild"
        verbose_name_plural = "Gegenstand-Bilder"

    def __str__(self):
        return f"Bild für {self.gegenstand.titel}"

class Chat(models.Model):
    gegenstand = models.ForeignKey(Gegenstand, on_delete=models.CASCADE, related_name='chats')
    kunde = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kunden_chats')
    mitarbeiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mitarbeiter_chats', null=True, blank=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat zu: {self.gegenstand.titel} ({self.kunde.username})"

class Nachricht(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='nachrichten')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    gesendet_am = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Von {self.sender.username} am {self.gesendet_am.strftime('%d.%m.%Y %H:%M')}"

class Bericht(models.Model):
    gegenstand = models.OneToOneField(Gegenstand, on_delete=models.CASCADE, related_name='bericht')
    mitarbeiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='erstellte_berichte')
    notizen = models.TextField()
    abgeholt_von = models.CharField(max_length=200, blank=True)
    abgeholt_am = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Abschlussbericht für: {self.gegenstand.titel}"