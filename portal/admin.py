from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Gegenstand, ChatRoom, ChatMessage, UebergabeBericht


# Das Profil direkt in die normale Benutzerverwaltung einbetten
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Rollen-Profil'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_rolle')

    def get_rolle(self, obj):
        return obj.profile.get_rolle_display() if hasattr(obj, 'profile') else 'Keine Rolle'

    get_rolle.short_description = 'Benutzerrolle'


# Standard-User-Admin austauschen
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Unsere neuen Fundbüro-Modelle registrieren
@admin.register(Gegenstand)
class GegenstandAdmin(admin.ModelAdmin):
    list_display = ('titel', 'fundort', 'funddatum', 'status', 'google_form_id')
    list_filter = ('status', 'funddatum')
    search_fields = ('titel', 'beschreibung', 'fundort')


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('gegenstand', 'kunde', 'erstellt_am')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('raum', 'sender', 'gesendet_am')


@admin.register(UebergabeBericht)
class UebergabeBerichtAdmin(admin.ModelAdmin):
    list_display = ('gegenstand', 'kunde', 'bearbeiter', 'uebergabe_datum')