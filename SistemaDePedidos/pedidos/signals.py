from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Pedido

@receiver(post_save, sender=Pedido)
def enviar_notificacion_estado(sender, instance, created, **kwargs):
    if created:
        return  # Solo queremos notificar si el pedido EXISTE y cambia de estado

    # Detectar si el estado cambió
    try:
        old_instance = Pedido.objects.get(pk=instance.pk)
    except Pedido.DoesNotExist:
        old_instance = None

    if old_instance and old_instance.estado != instance.estado:
        # --- Construimos el email según el nuevo estado ---
        estados_texto = {
            "PENDIENTE": "tu pedido fue recibido y está en espera.",
            "EN_PREPARACION": "tu pedido está siendo preparado",
            "VIAJANDO": "tu pedido ya está en camino",
            "ENTREGADO": "tu pedido fue entregado ¡Gracias por tu compra!",
        }

        asunto = f"Actualización de tu pedido #{instance.id} — Fenrir PC"
        mensaje_html = render_to_string("emails/notificacion_estado.html", {
            "pedido": instance,
            "estado_texto": estados_texto.get(instance.estado, "actualizado"),
            "usuario": instance.usuario,
        })
        mensaje_texto = strip_tags(mensaje_html)

        email = EmailMultiAlternatives(
            subject=asunto,
            body=mensaje_texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.usuario.email],
        )
        email.attach_alternative(mensaje_html, "text/html")
        email.send(fail_silently=True)
