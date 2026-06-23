from django.contrib import admin
from .models import Profil, Gegenstand, GegenstandBild, Chat, Nachricht, Bericht

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'ist_mitarbeiter', 'telefonnummer')
    list_filter = ('ist_mitarbeiter',)

class GegenstandBildInline(admin.TabularInline):
    model = GegenstandBild
    extra = 1

@admin.register(Gegenstand)
class GegenstandAdmin(admin.ModelAdmin):
    list_display = ('titel', 'status', 'fundort', 'funddatum', 'erstellt_am')
    list_filter = ('status', 'funddatum')
    search_fields = ('titel', 'beschreibung', 'fundort')
    inlines = [GegenstandBildInline]

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
    # Hier sind jetzt die exakt korrekten Feldnamen aus deinem Modell eingetragen:
    list_display = ('gegenstand', 'mitarbeiter', 'abholer_name', 'ausgehaendigt_am')
    list_filter = ('ausgehaendigt_am',)