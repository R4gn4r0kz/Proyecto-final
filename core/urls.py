# core/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (index, 
                   categoria_juegos,
                   perfil_usuario,
                   iniciar_sesion,
                   cerrar_sesion,
                   register_view,
                   registrar_m,)

urlpatterns = [
    # Página de inicio
    path('', index, name='inicio'),

    # Juegos por categoría
    path('categoria/<slug:slug>/', categoria_juegos, name='categoria-juegos'),

    # Registro
    path('registrarse/', register_view, name='registrarse'),
    path('registrar/',    registrar_m,   name='registrar'),

    # Login / Logout
    path('login/',  iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion,  name='logout'),

    # Perfil de usuario
    path('perfil/', perfil_usuario, name='perfil_usuario'),
]
