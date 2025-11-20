from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    telefono = forms.CharField(max_length=20, required=True, label="Número de teléfono")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "telefono",
            "password1",
            "password2"
        ]
