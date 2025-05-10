# core/forms.py
from django import forms
from django.contrib.auth.models import User
from shop.models import UsuarioProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        min_length=4,
        help_text="Como mínimo 4 caracteres."
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get("password") != cd.get("password2"):
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cd["password2"]

class PerfilForm(forms.ModelForm):
    class Meta:
        model = UsuarioProfile
        fields = ['tipo_usuario', 'direccion']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']