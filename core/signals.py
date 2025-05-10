# core/signals.py

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import UsuarioProfile, TipoUsuario

User = get_user_model()

@receiver(post_save, sender=User)
def crear_o_guardar_perfil(sender, instance, created, **kwargs):
    """
    Al crear un nuevo usuario, le asignamos un perfil con tipo_usuario por defecto.
    Si el perfil ya existe, simplemente lo guardamos.
    """
    if created:
        # Obtenemos el TipoUsuario por defecto ('cliente') o el primero disponible
        default_tipo = TipoUsuario.objects.filter(nombre='cliente').first()
        if default_tipo is None:
            default_tipo = TipoUsuario.objects.first()
        # Creamos el perfil con el tipo_usuario por defecto
        UsuarioProfile.objects.create(user=instance, tipo_usuario=default_tipo)
    else:
        try:
            perfil = instance.profile
        except UsuarioProfile.DoesNotExist:
            # Por si no existiese aún (rare case), lo creamos igualmente
            default_tipo = TipoUsuario.objects.filter(nombre='cliente').first() or TipoUsuario.objects.first()
            UsuarioProfile.objects.create(user=instance, tipo_usuario=default_tipo)
        else:
            # Guardamos los cambios (por ejemplo, last_login)
            perfil.save()
