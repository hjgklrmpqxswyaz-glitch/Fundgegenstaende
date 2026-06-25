from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Hier war der Fehler: urls statt url
    path('admin/', admin.site.urls),

    # Die URLs deiner Fundbüro-App
    path('gegenstaende/', include('portal.urls')),

    # Djangos eingebaute Auth-URLs (login, logout, passwort-änderung etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Startseite direkt auf die Gegenstände weiterleiten
    path('', lambda request: redirect('gegenstand_liste', permanent=False)),
]