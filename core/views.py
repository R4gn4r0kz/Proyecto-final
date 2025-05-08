# prototipo/core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from shop.models import Direccion, Region, Comuna, TipoUsuario, UsuarioProfile, Categoria
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.crypto import get_random_string
from shop.models import PasswordResetToken

User = get_user_model()

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
    shop_categories = Categoria.objects.all()
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
    comunas = Comuna.objects.all()
    return render(request, 'core/registrarse.html', {
        'shop_categories': shop_categories,
        'regiones_m': regiones,
        'comunas_m': comunas
    })

def registrar_m(request):
    """
    Procesa el formulario de registro: crea User, Direccion, UsuarioProfile.
    """
    if request.method != 'POST':
        return redirect('registrarse')

    # Captura de datos del formulario
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    region_id = request.POST.get('region')
    comuna_id = request.POST.get('comuna')
    direccion_text = request.POST.get('direccion')

    # Obtención de instancias relacionadas
    try:
        region_obj = Region.objects.get(pk=region_id)
        comuna_obj = Comuna.objects.get(pk=comuna_id)
    except (Region.DoesNotExist, Comuna.DoesNotExist):
        messages.error(request, 'Región o comuna no válidas.')
        return redirect('registrarse')

    # Tipo de usuario: ID 2 = Cliente
    try:
        tipo_user = TipoUsuario.objects.get(pk=2)
    except TipoUsuario.DoesNotExist:
        messages.error(request, 'Tipo de usuario no configurado.')
        return redirect('registrarse')

    # Verificar existencia de usuario
    if User.objects.filter(username=username).exists():
        messages.error(request, 'El usuario ya existe')
        return redirect('registrarse')

    # Crear usuario (hashea contraseña)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.first_name = nombre
    user.last_name = apellido
    user.save()

    # Crear dirección
    direccion_obj = Direccion.objects.create(
        descripcion=direccion_text,
        comuna=comuna_obj
    )

    # Crear perfil
    UsuarioProfile.objects.create(
        user=user,
        tipo_usuario=tipo_user,
        direccion=direccion_obj
    )

    messages.success(request, 'Cuenta creada correctamente.')
    return redirect('login')

def iniciar_sesion(request):
    """
    Autentica y loguea al usuario.
    """
    if request.method == 'POST':
        # Asegúrate de usar los mismos 'name' que en tu <input> de inicio de sesión:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'core/inicio_sesion.html', {
    'shop_categories': shop_categories,
})


def cerrar_sesion(request):
    """
    Cierra la sesión del usuario y lo redirige al login.
    """
    auth.logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

def recuperar_contraseña(request):
    mensaje = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Genera un token único
            token = get_random_string(64)
            # Guarda el token en la base de datos
            PasswordResetToken.objects.create(user=user, token=token)
            # Construye el link absoluto
            reset_link = request.build_absolute_uri(
                reverse('reset_confirm', args=[token])
            )
            # Envía el correo con reset_link...
            # send_mail( ... , html_message=f"Pincha aquí: {reset_link}", ...)
            mensaje = 'Revisa tu correo para continuar con la recuperación.'
        except User.DoesNotExist:
            mensaje = 'Ese email no está registrado.'

    return render(request, 'core/recuperar_contrasena.html', {'mensaje': mensaje})

def reset_confirm(request, token):
    contexto = {}
    try:
        pr = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        contexto['error'] = 'Enlace inválido o expirado.'
        return render(request, 'reset_confirm.html', contexto)

    if request.method == 'POST':
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        if pw1 and pw1 == pw2:
            # Guarda la nueva contraseña
            pr.user.password = make_password(pw1)
            pr.user.save()
            pr.delete()  # invalida el token
            return redirect('login')  # o a la URL que uses para el login
        else:
            contexto['error'] = 'Las contraseñas no coinciden.'

    return render(request, 'reset_confirm.html', contexto)