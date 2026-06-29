import os
import django
import csv
from datetime import datetime

# Setup für Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundbuero_project.settings')
django.setup()

from portal.models import Gegenstand, GegenstandBild


def import_csv_data(filepath):
    # Vor dem Import alle existierenden Daten löschen, um Duplikate/alte Links zu vermeiden
    GegenstandBild.objects.all().delete()
    Gegenstand.objects.all().delete()

    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Datum parsen
            try:
                datum = datetime.strptime(row['An welchem Tag wurde der Gegenstand gefunden?'], "%d.%m.%Y").date()
            except:
                datum = datetime.now().date()

            # Gegenstand erstellen
            g = Gegenstand.objects.create(
                bezeichnung=row['In welchem Bus wurde der Gegenstand gefunden'],
                fundort=row['Auf welcher Linie wurde der Gegenstand gefunden'],
                funddatum=datum,
                beschreibung=row['Beschreibung des Fundgegenstandes']
            )

            # Bilder verarbeiten und URL transformieren
            bild_urls = row.get('Bild bzw. Bilder', '').split(',')
            for url in bild_urls:
                raw_url = url.strip()
                if raw_url:
                    # Umwandlung: open?id= -> uc?export=view&id=
                    final_url = raw_url.replace('open?id=', 'uc?export=view&id=')
                    GegenstandBild.objects.create(gegenstand=g, bild_url=final_url)

            print(f"Erfolgreich importiert: {g.bezeichnung}")


if __name__ == "__main__":
    import_csv_data('antworten.csv')