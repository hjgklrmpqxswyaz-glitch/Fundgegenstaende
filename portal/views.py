from django.shortcuts import render
from .models import Gegenstand


def gegenstand_liste(request):
    # Wir holen alle Gegenstände und laden die verknüpften Bilder direkt mit (optimiert die Performance)
    gegenstaende = Gegenstand.objects.prefetch_related('bilder').order_by('-erstellt_am')

    context = {
        'gegenstaende': gegenstaende,
    }
    return render(request, 'portal/gegenstand_liste.html', context)