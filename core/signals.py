# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from shop.models import UsuarioProfile, TipoUsuario, Direccion, Comuna
#from django.contrib.auth.models import User


User = get_user_model()

@receiver(post_save, sender=User)
def crear_o_guardar_perfil(sender, instance, created, **kwargs):
    if created:
        # obtén o crea aquí los defaults que necesites
        tipo_default, _ = TipoUsuario.objects.get_or_create(nombre='Cliente estándar')
        comuna_default = Comuna.objects.first()
        direccion_default, _ = Direccion.objects.get_or_create(
            descripcion='Sin dirección',
            comuna=comuna_default
        )
        UsuarioProfile.objects.create(
            user=instance,
            tipo_usuario=tipo_default,
            direccion=direccion_default
        )
    else:
        instance.profile.save()
