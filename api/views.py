# api/views.py
import json, requests
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.forms import PasswordResetForm
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from shop.models import Juego, Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer, JuegoSerializer
from django.views.decorators.csrf import csrf_exempt


class CategoriaListAPI(generics.ListAPIView):
    queryset         = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset         = Producto.objects.all()
    serializer_class = ProductoSerializer

def ping(request):
    return JsonResponse({'status': 'pong'})

# API propia: lista de juegos
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

# API para recuperar contraseña
@csrf_exempt
def password_reset_api(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        data = json.loads(request.body)
        form = PasswordResetForm({'email': data.get('email', '')})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    if form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            email_template_name='core/password_reset_email.html',
            subject_template_name='core/password_reset_subject.txt',
        )
        return JsonResponse({'detail': 'Se ha enviado el email de recuperación.'})
    else:
        return JsonResponse(form.errors, status=400)

# API que consume servicio externo RAWG
@csrf_exempt
def rawg_populares_api(request):
    """
    Trae los juegos más populares de RAWG (servicio externo)
    y devuelve sus nombres y ratings.
    """
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    # Tu API key en settings o variable de entorno
    from django.conf import settings
    api_key = settings.RAWG_API_KEY
    url = f'https://api.rawg.io/api/games?key={api_key}&ordering=-rating&page_size=10'
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        return JsonResponse({'error': 'RAWG API falló'}, status=502)
    data = resp.json().get('results', [])
    salida = [
        {'name': juego['name'], 'rating': juego['rating']}
        for juego in data
    ]
    return JsonResponse({'rawg_populares': salida})
