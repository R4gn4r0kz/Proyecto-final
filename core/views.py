# prototipo/core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()
from shop.models import Direccion, Region, Comuna, TipoUsuario

@login_required
def perfil_usuario(request):
    perfil = getattr(request.user, 'profile', None)
    return render(request, 'core/perfil_usuario.html', {
        'user': request.user,
        'perfil': perfil,
    })


# Lista de categorías del navbar
shop_categories = [
    {'slug': 'accion',     'nombre': 'Acción'},
    {'slug': 'aventuras',  'nombre': 'Aventuras'},
    {'slug': 'terror',     'nombre': 'Terror'},
    {'slug': 'carreras',   'nombre': 'Carreras'},
    {'slug': 'estrategia', 'nombre': 'Estrategia'},
]

def index(request):
    """
    Página de inicio con listado de categorías.
    """
    return render(request, 'core/index.html', {
        'shop_categories': shop_categories
    })

def categoria_juegos(request, slug):
    """
    Muestra los juegos de la categoría `slug`.
    """
    return render(request, 'core/index.html', {
        'shop_categories': shop_categories,
        'current_category': slug
    })

def register_view(request):
    """
    Renderiza el formulario de registro.
    """
    regiones = Region.objects.all()
    comunas  = Comuna.objects.all()
    return render(request, 'core/registrarse.html', {
        'shop_categories': shop_categories,
        'regiones_m': regiones,
        'comunas_m': comunas
    })

# Creación de un nuevo usuario y su dirección
def registrar_m(request):
    if request.method != 'POST':
        return redirect('registrarse')

    # Captura de datos del formulario
    username = request.POST.get('usuario')
    password = request.POST.get('contra')
    email    = request.POST.get('email')
    region_id  = request.POST.get('region')
    comuna_id  = request.POST.get('comuna')
    nombre     = request.POST.get('nombre')
    apellido   = request.POST.get('apellido')
    direccion  = request.POST.get('direccion')

    # Obtención de instancias relacionadas
    region_obj   = Region.objects.get(idRegion=region_id)
    comuna_obj   = Comuna.objects.get(idComuna=comuna_id)
    tipo_user    = TipoUsuario.objects.get(idTipoUsuario=2)

    # Verificar existencia
    if User.objects.filter(username=username).exists():
        messages.error(request, 'El usuario ya existe')
        return redirect('registrarse')

    # Creación de usuario
    usuario_obj = User.objects.create(
        username=username,
        contrasennia=password,
        nombre=nombre,
        apellido=apellido,
        email=email,
        tipousuario=tipo_user
    )
    # Creación de dirección
    Direccion.objects.create(
        descripcionDir=direccion,
        usuario=usuario_obj,
        region=region_obj
    )

    messages.success(request, 'Cuenta creada correctamente.')
    return redirect('login')

def iniciar_sesion(request):
    """
    Autentica y loguea al usuario.
    """
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('contra')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'core/inicio_sesion.html')


def cerrar_sesion(request):
    """
    Cierra la sesión del usuario y lo redirige al login.
    """
    auth.logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')