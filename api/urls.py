# api/urls.py

from django.urls import path
from .views import (JuegoListAPI, 
                    JuegoDetailAPI, 
                    CategoriaListAPI,
                    password_reset_api,
                    rawg_populares_api)

urlpatterns = [
    path('juegos/',        JuegoListAPI.as_view(),   name='juego-list'), # API propia de juegos en BD
    path('juegos/<int:pk>/', JuegoDetailAPI.as_view(), name='juego-detail'), # GET detalle
    path('categorias/', CategoriaListAPI.as_view(), name='categoria-list'),    
    path('password-reset/', password_reset_api, name='api_password_reset'), # API de recuperación de contraseña
    path('external/rawg-populares/', rawg_populares_api, name='api_rawg_populares'), # API que consume servicio externo RAWG
]