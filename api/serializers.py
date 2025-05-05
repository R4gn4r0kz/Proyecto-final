# api/serializers.py
from rest_framework import serializers
from shop.models import Juego, Categoria, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Categoria
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Producto
        fields = ['id', 'categoria', 'nombre', 'precio']

class JuegoSerializer(serializers.ModelSerializer):
    cover     = serializers.CharField(read_only=True)
    categoria = serializers.IntegerField(source='categoria.id', read_only=True)
    class Meta:
        model  = Juego
        fields = ['id','titulo','resumen','cover','categoria']
