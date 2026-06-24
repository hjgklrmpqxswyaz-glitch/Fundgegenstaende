from django.shortcuts import render
from .models import Gegenstand
from django.db.models import Q

def gegenstand_liste(request):
    # 1. Nur Gegenstände holen, die NICHT den Status 'rueckgegeben' haben
    gegenstaende = Gegenstand.objects.exclude(status='rueckgegeben')

    # 2. Suchbegriff für Text (Titel / Beschreibung) auswerten
    suchbegriff = request.GET.get('q', '').strip()
    if suchbegriff:
        gegenstaende = gegenstaende.filter(
            Q(titel__icontains=suchbegriff) | Q(beschreibung__icontains=suchbegriff)
        )

    # 3. Filter für Bus-Linie / Fundort auswerten
    linie_filter = request.GET.get('linie', '').strip()
    if linie_filter:
        gegenstaende = gegenstaende.filter(fundort__icontains=linie_filter)

    # 4. Filter für Datum auswerten
    datum_filter = request.GET.get('datum', '').strip()
    if datum_filter:
        gegenstaende = gegenstaende.filter(funddatum__icontains=datum_filter)

    # Die bereinigte und gefilterte Liste an das Template übergeben
    context = {
        'gegenstaende': gegenstaende,
        'suchbegriff': suchbegriff,
        'linie_filter': linie_filter,
        'datum_filter': datum_filter,
    }
    return render(request, 'portal/gegenstand_liste.html', context)