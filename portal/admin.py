from django.contrib import admin
from .models import Gegenstand, GegenstandBild, TicketNachricht


class GegenstandBildInline(admin.TabularInline):
    model = GegenstandBild
    extra = 1


@admin.register(Gegenstand)
class GegenstandAdmin(admin.ModelAdmin):
    list_display = ('bezeichnung', 'fundort', 'funddatum', 'status', 'ist_abgelaufen_ampel')
    list_filter = ('status', 'funddatum', 'fundort')
    search_fields = ('bezeichnung', 'beschreibung', 'fundort')
    inlines = [GegenstandBildInline]

    def ist_abgelaufen_ampel(self, obj):
        return obj.ist_abgelaufen()

    ist_abgelaufen_ampel.boolean = True
    ist_abgelaufen_ampel.short_description = "Über 1 Jahr alt?"


@admin.register(TicketNachricht)
class TicketNachrichtAdmin(admin.ModelAdmin):
    list_display = ('gegenstand', 'kunde', 'absender', 'gesendet_am')
    list_filter = ('gesendet_am', 'absender')
    search_fields = ('inhalt', 'gegenstand__bezeichnung', 'kunde__email')


admin.site.register(GegenstandBild)