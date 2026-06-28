from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin-Oberfläche von Django
    path('admin/', admin.site.get_admin_urls() if hasattr(admin.site, 'get_admin_urls') else admin.site.urls),

    # Integrierte Django-Authentifizierung (aktiviert Verweise wie {% url 'logout' %})
    path('accounts/', include('django.contrib.auth.urls')),

    # Haupt-Routing für deine Fundbüro-App 'portal'
    path('', include('portal.urls')),
]