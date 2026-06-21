from django.contrib import admin
from .models import Profil, Gegenstand, GegenstandBild, Chat, Nachricht, Bericht

# Erlaubt es, Bilder direkt innerhalb der Gegenstand-Ansicht zu bearbeiten und anzusehen
class GegenstandBildInline(admin.StackedInline):
    model = GegenstandBild
    extra = 1  # Zeigt standardmäßig ein leeres Zusatzfeld für neue Bilder an
    max_num = 5  # Begrenzt die maximale Anzahl an Bildern im Admin-Interface auf 5

@admin.register(Gegenstand)
class GegenstandAdmin(admin.ModelAdmin):
    list_display = ('titel', 'fundort', 'funddatum', 'status', 'erstellt_am')
    list_filter = ('status', 'erstellt_am')
    search_fields = ('titel', 'beschreibung', 'fundort')
    inlines = [GegenstandBildInline]

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'ist_mitarbeiter')
    list_filter = ('ist_mitarbeiter',)
    search_fields = ('user__username', 'user__email')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('gegenstand', 'kunde', 'mitarbeiter', 'erstellt_am')
    list_filter = ('erstellt_am',)

@admin.register(Nachricht)
class NachrichtAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'gesendet_am')
    list_filter = ('gesendet_am',)

@admin.register(Bericht)
class BerichtAdmin(admin.ModelAdmin):
    list_display = ('gegenstand', 'mitarbeiter', 'abgeholt_von', 'abgeholt_am')