# shop/urls.py
from django.urls import path
from .views import tienda_index, juego_detail, categoria_detail

urlpatterns = [
    path('', tienda_index, name='shop_index'),
    path('juego/<int:id>/', juego_detail, name='juego_detail'),
    path('categoria/<int:id>/', categoria_detail, name='shop_categoria'),
]

