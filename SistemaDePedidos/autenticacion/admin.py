# autenticacion/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PerfilUsuario

# Inline para ver/editar el teléfono directamente desde User
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de usuario'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_telefono', 'is_staff')

    def get_telefono(self, obj):
        # Si el usuario no tiene perfil, evita el error
        return getattr(obj.perfilusuario, 'telefono', '-')
    get_telefono.short_description = 'Teléfono'

# Re-registramos el modelo User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
