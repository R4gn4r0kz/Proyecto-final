# shop/models.py

from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug   = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Si no tiene slug, lo generamos a partir del nombre
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Para poder usar {{ cat.get_absolute_url }} en plantillas
        return reverse('categoria-juegos', args=[self.slug])

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        related_name='productos',
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Juego(models.Model):
    titulo = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", max_length=200, unique=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    resumen = models.TextField("Resumen corto", blank=True)
    descripcion = models.TextField("Descripción completa", blank=True)
    cover = models.URLField("Portada")
    fecha_lanzamiento = models.DateField(
        "Fecha de lanzamiento",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_lanzamiento", "titulo"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tipo de usuario")

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Comuna")

    def __str__(self):
        return self.nombre

class Region(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Región")
    comuna = models.ForeignKey(
        Comuna,
        on_delete=models.PROTECT,
        related_name='regiones'
    )

    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    descripcion = models.TextField(verbose_name="Dirección")
    comuna = models.ForeignKey(
        Comuna,
        on_delete=models.PROTECT,
        related_name='direcciones'
    )

    def __str__(self):
        return self.descripcion

class UsuarioProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    tipo_usuario = models.ForeignKey(
        TipoUsuario,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfiles'
    )

    def __str__(self):
        return f"{self.user.username} – {self.tipo_usuario.nombre}"

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} – {self.token}"
