# api/views.py
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, generics
from shop.models import Juego, Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer, JuegoSerializer

class CategoriaListAPI(generics.ListAPIView):
    queryset         = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset         = Producto.objects.all()
    serializer_class = ProductoSerializer

def ping(request):
    return JsonResponse({'status': 'pong'})

class JuegoListAPI(generics.ListAPIView):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer

class JuegoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer

class JuegoDetailAPI(generics.RetrieveAPIView):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer