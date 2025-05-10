# core/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from .views import (index, 
                   categoria_juegos,
                   perfil_usuario,
                   iniciar_sesion,
                   cerrar_sesion,
                   register_view,
                   registrar_m,
                   editar_perfil,)
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
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Editar perfil de usuario
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # Eliminar perfil de usuario
    path('perfil/eliminar/', views.eliminar_perfil, name='eliminar_perfil'),

    # Recuperar contraseña
    #path('recuperar-password/', views.recuperar_contraseña, name='recuperar_contrasena'),
    #path('reset/<str:token>/', views.reset_confirm, name='reset_confirm'),

    # 1. Formulario para solicitar el enlace de recuperación
    path(
        'recuperar-contrasena/',
        auth_views.PasswordResetView.as_view(
            template_name='core/recuperar_contrasena.html',
            email_template_name='core/password_reset_email.html',
            subject_template_name='core/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset'
    ),

    # 2. Página que confirma que el correo fue enviado
    path(
        'recuperar-contrasena/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='core/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # 3. Formulario para establecer la nueva contraseña
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='core/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm'
    ),

    # 4. Página final que confirma el cambio de contraseña
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='core/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
  
]
