# api/views.py
from django.shortcuts import render
from rest_framework.generics import ListAPIView
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
    serializer_class = JuegoSerializer
    pagination_class   = None    # ← Así Django REST vuelve todo el queryset de golpe

    def get_queryset(self):
        raw = self.request.query_params.get('categoria')
        try:
             cid = int(raw)
        except (TypeError, ValueError):
             return Juego.objects.all()  # ← quitas [:5] para que devuelva los 25
        return Juego.objects.filter(categoria_id=cid)  # ← aquí también quitas [:5]

class JuegoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer

class JuegoDetailAPI(generics.RetrieveAPIView):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer