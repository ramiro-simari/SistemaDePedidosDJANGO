from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        help_text="Requerido. Ingresá una dirección de correo válida.",
        widget=forms.EmailInput(attrs={'placeholder': 'tuemail@ejemplo.com'})
    )
    first_name = forms.CharField(
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre'})
    )
    last_name = forms.CharField(
        required=True,
        label="Apellido",
        widget=forms.TextInput(attrs={'placeholder': 'Tu apellido'})
    )
    telefono = forms.CharField(
        required=True,
        label="Teléfono",
        help_text="Requerido. Ingresá un número válido.",
        widget=forms.TextInput(attrs={'placeholder': '+54 9 11 2345-6789'})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "telefono", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            # Guardar teléfono en el perfil
            user.perfilusuario.telefono = self.cleaned_data["telefono"]
            user.perfilusuario.save()

        return user
