from django.contrib import admin
from django.contrib.auth.models import User
from .models import Perfil

class PerfilInline(admin.StackedInline):
    model = Perfil
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [PerfilInline]

    # 👉 Ahora mostramos si es superuser
    list_display = ("username", "email", "get_telefono", "is_superuser")

    def get_telefono(self, obj):
        return obj.perfil.telefono
    get_telefono.short_description = "Teléfono"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
