# shop/context_processors.py
from .models import Categoria

def shop_categories(request):
    return {
        'shop_categories': Categoria.objects.all()
    }
