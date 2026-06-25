from django.contrib import admin
from .models import Gegenstand, GegenstandBild, Nachricht

# Erlaubt es, Bilder direkt in der Gegenstands-Ansicht im Admin-Bereich zu sehen
class GegenstandBildInline(admin.TabularInline):
    model = GegenstandBild
    extra = 1

@admin.register(Gegenstand)
class GegenstandAdmin(admin.ModelAdmin):
    list_display = ('titel', 'fundort', 'funddatum', 'status')
    list_filter = ('status', 'funddatum')
    search_fields = ('titel', 'beschreibung', 'fundort')
    inlines = [GegenstandBildInline]

@admin.register(Nachricht)
class NachrichtAdmin(admin.ModelAdmin):
    list_display = ('gegenstand', 'absender', 'zeitstempel')
    list_filter = ('zeitstempel', 'absender')
    search_fields = ('text', 'absender__username', 'gegenstand__titel')