# shop/views.py
from django.shortcuts import render, get_object_or_404
from .models import Juego

def tienda_index(request):
    # sólo renderiza un template mínimo
    return render(request, 'shop/tienda_index.html', {})

def juego_detail(request, id):
    juego = get_object_or_404(Juego, id=id)
    return render(request, 'shop/juego_detail.html', {'juego': juego})

def categoria_detail(request, id):
    # opcionalmente pasar juegos ya filtrados al template
    return render(request, 'shop/categoria.html', {'categoria_id': id})
