from django.urls import path
from . import views

urlpatterns = [
    # Übersicht der Fundgegenstände für Kunden
    path('', views.gegenstand_liste, name='gegenstand_liste'),

    # Detailansicht und Chat-System (Mitarbeiter & Kunden)
    path('gegenstand/<int:pk>/', views.gegenstand_detail, name='gegenstand_detail'),

    # Disponenten-Zentrum (Dashboard)
    path('dashboard/', views.mitarbeiter_dashboard, name='mitarbeiter_dashboard'),

    # Prozesse für die Übergabe und Entsorgung
    path('gegenstand/<int:pk>/uebergabe/', views.uebergabe_erfassen, name='uebergabe_erfassen'),
    path('gegenstand/<int:pk>/drucken/', views.uebergabeschein_drucken, name='uebergabeschein_drucken'),
    path('gegenstand/<int:pk>/entsorgen/', views.gegenstand_entsorgen, name='gegenstand_entsorgen'),

    # API-Webhook für die Echtzeit-Aktualisierung aus Google Forms
    path('api/google-webhook/', views.google_form_webhook, name='google_webhook'),

    # Füge diese beiden Pfade in deine urlpatterns-Liste ein:
    path('accounts/profile/', views.login_redirect_view, name='login_redirect'),
    path('accounts/register/', views.register_view, name='register'),
]