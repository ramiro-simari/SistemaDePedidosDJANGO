from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import FormularioContacto

def contacto(request):
    formulario_contacto = FormularioContacto()

    if request.method == "POST":
        formulario_contacto = FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre = formulario_contacto.cleaned_data.get("nombre")
            email_usuario = formulario_contacto.cleaned_data.get("email")
            contenido = formulario_contacto.cleaned_data.get("contenido")

            # Crear el email
            email = EmailMessage(
                subject="Mensaje desde App Django",
                body=f"El usuario {nombre} con la dirección {email_usuario} escribió:\n\n{contenido}",
                from_email="ramirosimari26@gmail.com",  # Usa el DEFAULT_FROM_EMAIL definido en settings.py
                to=["ramirosimari26@gmail.com"],
                reply_to=[email_usuario],
            )

            try:
                email.send()
                return redirect("/contacto/?valido")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")  # útil para debug
                return redirect("/contacto/?novalido")

    return render(request, "contacto/contacto.html", {"miFormulario": formulario_contacto})
