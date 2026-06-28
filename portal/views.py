import json
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from .models import Gegenstand, GegenstandBild


# --- Webhook mit Debugging ---
@csrf_exempt
def google_form_webhook(request):
    print(f"DEBUG: Webhook empfangen! Methode: {request.method}")
    if request.method == 'POST':
        try:
            body_content = request.body.decode('utf-8')
            print(f"DEBUG: Body Inhalt: {body_content}")

            data = json.loads(body_content)
            datum_str = data.get('funddatum', '')
            datum_obj = datetime.strptime(datum_str, "%d.%m.%Y").date() if datum_str else None

            g = Gegenstand.objects.create(
                bezeichnung=data.get('bezeichnung', 'Unbekannt'),
                fundort=data.get('fundort', 'Unbekannt'),
                funddatum=datum_obj,
                beschreibung=data.get('beschreibung', ''),
                rohe_bild_urls=data.get('bild bzw. bilder', '')
            )
            print(f"DEBUG: Gegenstand erstellt mit ID: {g.id}")

            url_string = data.get('bild bzw. bilder', '')
            if url_string:
                urls = [u.strip() for u in url_string.split(',')]
                for url in urls:
                    if url:
                        GegenstandBild.objects.create(gegenstand=g, bild_url=url)

            return JsonResponse({'status': 'success'}, status=201)
        except Exception as e:
            print(f"DEBUG: Fehler im Webhook: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid_method'}, status=405)


# --- Registrierung & Login ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('gegenstand_liste')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@staff_member_required
def login_redirect_view(request):
    if request.user.is_staff:
        return redirect('mitarbeiter_dashboard')
    return redirect('gegenstand_liste')


# --- Öffentliche Ansichten ---
def gegenstand_liste(request):
    gegenstaende = Gegenstand.objects.all().order_by('-erstellt_am')
    return render(request, 'portal/gegenstand_liste.html', {'gegenstaende': gegenstaende})


def gegenstand_detail(request, pk):
    gegenstand = get_object_or_404(Gegenstand, pk=pk)
    return render(request, 'portal/gegenstand_detail.html', {'gegenstand': gegenstand})


# --- Mitarbeiter-Ansichten ---
@staff_member_required
def mitarbeiter_dashboard(request):
    gegenstaende = Gegenstand.objects.all().order_by('-erstellt_am')
    return render(request, 'portal/mitarbeiter_dashboard.html', {'gegenstaende': gegenstaende})


@staff_member_required
def uebergabe_erfassen(request, pk):
    gegenstand = get_object_or_404(Gegenstand, pk=pk)
    return render(request, 'portal/uebergabe_form.html', {'gegenstand': gegenstand})


@staff_member_required
def uebergabeschein_drucken(request, pk):
    gegenstand = get_object_or_404(Gegenstand, pk=pk)
    return HttpResponse(f"Druckansicht für {gegenstand.bezeichnung}")


@staff_member_required
def gegenstand_entsorgen(request, pk):
    gegenstand = get_object_or_404(Gegenstand, pk=pk)
    gegenstand.status = 'entsorgt'
    gegenstand.save()
    return redirect('mitarbeiter_dashboard')