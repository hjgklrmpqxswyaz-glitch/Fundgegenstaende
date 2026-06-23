from django.urls import path
from . import views

urlpatterns = [
    path('gegenstaende/', views.gegenstand_liste, name='gegenstand_liste'),
]