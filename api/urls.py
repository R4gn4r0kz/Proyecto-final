# api/urls.py

from django.urls import include, path
from .views import JuegoListAPI, JuegoDetailAPI, CategoriaListAPI

urlpatterns = [
    path('juegos/',        JuegoListAPI.as_view(),   name='juego-list'),   # GET lista
    path('juegos/<int:pk>/', JuegoDetailAPI.as_view(), name='juego-detail'), # GET detalle
    path('categorias/', CategoriaListAPI.as_view(), name='categoria-list'),

]