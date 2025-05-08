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
from . import views

urlpatterns = [
    # Página de inicio
    path('', index, name='inicio'),

    # Juegos por categoría
    path('categoria/<slug:slug>/', categoria_juegos, name='categoria-juegos'),

    # Registro
    path('registrarse/', register_view, name='registrarse'), # GET → muestra el formulario
    path('registrar/',    registrar_m,   name='registrar_m'),  # POST → procesa el envío

    # Login / Logout
    path('login/',  iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion,  name='logout'),

    # Perfil de usuario
    path('perfil/', perfil_usuario, name='perfil_usuario'),

    # Recuperar contraseña
    path('recuperar-password/', views.recuperar_contraseña, name='recuperar_contrasena'),
    path('reset/<str:token>/', views.reset_confirm, name='reset_confirm'),

]
