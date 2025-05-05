# shop/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (
    UsuarioProfile,
    TipoUsuario,
    Region,
    Comuna,
    Direccion,
    Categoria,
    Producto,
    Genero,
    Juego,
)

# Inline para que, al editar un User, aparezca su perfil
class UsuarioProfileInline(admin.StackedInline):
    model = UsuarioProfile
    can_delete = False
    verbose_name_plural = 'Perfiles de Usuario'

# Extiende UserAdmin para incluir el perfil en línea
class CustomUserAdmin(UserAdmin):
    inlines = (UsuarioProfileInline,)

# Desregistra el User admin por defecto e instala el tuyo
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registra los demás modelos de shop
admin.site.register(TipoUsuario)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Direccion)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Genero)
admin.site.register(Juego)