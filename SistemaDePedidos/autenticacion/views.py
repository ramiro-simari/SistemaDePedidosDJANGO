from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormularioRegistro
from .models import PerfilUsuario


class VRegistro(View):

    def get(self, request):
        form = FormularioRegistro()
        return render(request, "registro/registro.html", {"form": form})

    def post(self, request):
        form = FormularioRegistro(request.POST)

        if form.is_valid():
            usuario = form.save()
            # Crear o actualizar el perfil del usuario
            perfil, creado = PerfilUsuario.objects.get_or_create(user=usuario)
            perfil.telefono = form.cleaned_data["telefono"]
            perfil.save()

            login(request, usuario)
            messages.success(request, "¡Tu cuenta fue creada correctamente!")
            return redirect("Home")

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request, "registro/registro.html", {"form": form})


def cerrar_sesion(request):
    logout(request)
    return redirect("Home")


def logear(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contra)

            if usuario is not None:
                login(request, usuario)
                return redirect("Home")
            else:
                messages.error(request, "Usuario no válido")
        else:
            messages.error(request, "Información incorrecta")

    form = AuthenticationForm()
    return render(request, "login/login.html", {"form": form})
