import os
import csv
import requests
from django.core.management.base import BaseCommand
from portal.models import Gegenstand, GegenstandBild


class Command(BaseCommand):
    help = 'Synchronisiert die Fundgegenstände inklusive mehrerer Bilder aus der Google Sheets CSV-URL'

    def handle(self, *args, **options):
        # 1. URL aus der .env Datei auslesen
        csv_url = os.getenv('GOOGLE_SHEET_CSV_URL')

        if not csv_url or 'YOUR_LINK_HERE' in csv_url:
            self.stdout.write(
                self.style.ERROR('Fehler: Keine gültige GOOGLE_SHEET_CSV_URL in der .env Datei gefunden!'))
            return

        self.stdout.write('Starte Download der Google-Sheets-Daten...')

        try:
            # CSV-Daten vom Google-Server abrufen
            response = requests.get(csv_url, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'
            lines = response.text.splitlines()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Fehler beim Herunterladen der Daten: {e}'))
            return

        if not lines:
            self.stdout.write(self.style.WARNING('Die empfangene CSV-Datei ist leer.'))
            return

        # 2. CSV-Reader initialisieren
        reader = csv.reader(lines)
        header = next(reader)  # Spaltennamen auslesen

        # Spalten-Indizes ermitteln
        idx_zeitstempel = -1
        idx_linie = -1
        idx_busnummer = -1
        idx_tag = -1
        idx_uhrzeit = -1
        idx_verbleib = -1
        idx_beschreibung = -1
        idx_bilder = -1

        for i, column in enumerate(header):
            column_lower = column.lower()
            if 'zeitstempel' in column_lower:
                idx_zeitstempel = i
            elif 'linie' in column_lower:
                idx_linie = i
            elif 'bus' in column_lower:
                idx_busnummer = i
            elif 'tag' in column_lower:
                idx_tag = i
            elif 'uhrzeit' in column_lower:
                idx_uhrzeit = i
            elif 'passiert' in column_lower or 'verbleib' in column_lower:
                idx_verbleib = i
            elif 'beschreibung' in column_lower:
                idx_beschreibung = i
            elif 'bild' in column_lower:
                idx_bilder = i

        # Überprüfung der Pflichtspalten
        if idx_zeitstempel == -1 or idx_beschreibung == -1:
            self.stdout.write(self.style.ERROR(
                "Fehler: 'Zeitstempel' oder 'Beschreibung des Fundgegenstandes' nicht gefunden."
            ))
            return

        anzahl_neu = 0
        anzahl_update = 0

        # 3. Daten zeilenweise verarbeiten
        for row in reader:
            if not row or len(row) <= max(idx_zeitstempel, idx_beschreibung):
                continue

            google_id = row[idx_zeitstempel].strip()
            titel = row[idx_beschreibung].strip()

            if not google_id or not titel:
                continue

            # Optionale Felder auslesen
            linie = row[idx_linie].strip() if idx_linie != -1 and idx_linie < len(row) else 'Unbekannt'
            busnummer = row[idx_busnummer].strip() if idx_busnummer != -1 and idx_busnummer < len(row) else 'Unbekannt'
            fundtag = row[idx_tag].strip() if idx_tag != -1 and idx_tag < len(row) else ''
            uhrzeit = row[idx_uhrzeit].strip() if idx_uhrzeit != -1 and idx_uhrzeit < len(row) else ''
            verbleib = row[idx_verbleib].strip() if idx_verbleib != -1 and idx_verbleib < len(row) else ''

            # Beschreibungstext zusammenbauen
            detail_beschreibung = (
                f"Bus-Linie: {linie}\n"
                f"Bus-Nummer: {busnummer}\n"
                f"Gefunden um: {uhrzeit} Uhr\n"
                f"Aktueller Verbleib des Gegenstands: {verbleib}"
            )

            # Gegenstand anlegen oder aktualisieren
            gegenstand, created = Gegenstand.objects.update_or_create(
                google_form_id=google_id,
                defaults={
                    'titel': titel,
                    'beschreibung': detail_beschreibung,
                    'fundort': f"Linie {linie} (Bus: {busnummer})",
                    'funddatum': fundtag if fundtag else google_id,
                }
            )

            if created:
                anzahl_neu += 1
            else:
                anzahl_update += 1

            # 4. Mehrfache Bilder verarbeiten (Spalte "Bild bzw. Bilder")
            if idx_bilder != -1 and idx_bilder < len(row):
                bilder_zelle = row[idx_bilder].strip()

                # Zuerst bestehende Bilder dieses Gegenstands löschen (verhindert Duplikate beim Re-Import)
                gegenstand.bilder.all().delete()

                if bilder_zelle:
                    # Die Links am Komma aufteilen
                    bild_links = [link.strip() for link in bilder_zelle.split(',') if link.strip()]

                    # Maximal 5 Bilder importieren
                    for link in bild_links[:5]:
                        GegenstandBild.objects.create(
                            gegenstand=gegenstand,
                            bild_url=link
                        )

        self.stdout.write(self.style.SUCCESS(
            f'Synchronisation erfolgreich! {anzahl_neu} neue Gegenstände hinzugefügt, '
            f'{anzahl_update} aktualisiert. Bilder wurden sauber zugeordnet.'
        ))