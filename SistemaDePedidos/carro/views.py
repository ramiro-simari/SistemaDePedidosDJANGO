from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from tienda.models import Producto
from pedidos.models import Pedido, LineaPedidos
from .carro import Carro


def agregar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Producto, id=producto_id)
    agregado = carro.agregar(producto=producto)

    if agregado:
        messages.success(request, f"{producto.nombre} agregado al carrito.")
    else:
        messages.warning(
            request,
            f"No hay suficiente stock disponible de {producto.nombre}. "
            f"Stock máximo: {producto.stock} unidades."
        )

    # Recordar abrir el offcanvas al recargar
    request.session["abrir_carrito"] = True
    return redirect(request.META.get("HTTP_REFERER", "Tienda"))


def eliminar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carro.eliminar(producto=producto)
    messages.info(request, f"{producto.nombre} eliminado del carrito.")
    request.session["abrir_carrito"] = True
    return redirect(request.META.get("HTTP_REFERER", "Tienda"))


def restar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carro.restar_producto(producto=producto)
    request.session["abrir_carrito"] = True
    return redirect(request.META.get("HTTP_REFERER", "Tienda"))


def limpiar_carro(request):
    carro = Carro(request)
    carro.limpiar_carro()
    messages.info(request, "Carrito vaciado correctamente.")
    request.session["abrir_carrito"] = True
    return redirect(request.META.get("HTTP_REFERER", "Tienda"))
# ----------------------------
# REALIZAR PEDIDO (flujo completo)
# ----------------------------
@login_required(login_url="/autenticacion/logear")
def realizar_pedido(request):
    carro = Carro(request)
    productos_fuera_de_stock = []

    # --- Verificar stock disponible ---
    for item in carro.carro.values():
        producto = Producto.objects.get(id=item["producto_id"])
        cantidad_pedida = item["cantidad"]

        if cantidad_pedida > producto.stock:
            productos_fuera_de_stock.append({
                "nombre": producto.nombre,
                "stock": producto.stock,
                "pedidos": cantidad_pedida,
            })

    if productos_fuera_de_stock:
        mensaje = "No se pudo realizar el pedido. Verifica los siguientes productos:\n"
        for p in productos_fuera_de_stock:
            mensaje += f"• {p['nombre']}: stock disponible {p['stock']}, en carrito {p['pedidos']}\n"
        messages.warning(request, mensaje)
        return redirect("Tienda")

    # --- Crear el pedido ---
    pedido = Pedido.objects.create(usuario=request.user)

    lineas_pedido = []
    for key, value in carro.carro.items():
        producto = Producto.objects.get(id=value["producto_id"])

        # Descontar stock
        producto.stock -= value["cantidad"]
        producto.save()

        # Crear línea de pedido
        lineas_pedido.append(
            LineaPedidos(
                pedido=pedido,
                producto=producto,
                cantidad=value["cantidad"],
                precio=producto.precio
            )
        )

    LineaPedidos.objects.bulk_create(lineas_pedido)

    # --- Enviar email de confirmación (HTML + texto) ---
    asunto = "Gracias por tu pedido — Fenrir PC - Tienda Gaming"
    template_name = "emails/pedido.html"
    total = sum([l.cantidad * l.precio for l in lineas_pedido])

    html_content = render_to_string(template_name, {
        "pedido": pedido,
        "lineas_pedido": lineas_pedido,
        "nombreusuario": request.user.username,
        "total": total,
    })
    text_content = strip_tags(html_content)

    from_email = settings.DEFAULT_FROM_EMAIL
    # Asegurar destino válido
    to_email = request.user.email.strip() if getattr(request.user, "email", None) else None
    if not to_email:
        to_email = "ramirosimari.dev@gmail.com"  # fallback admin o soporte

    print(f"Enviando correo de pedido a: {to_email}")

    email = EmailMultiAlternatives(
        subject=asunto,
        body=text_content,
        from_email=from_email,
        to=[to_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    # --- Enviar email al local (notificación interna) ---
    asunto_local = f"Nuevo pedido de {request.user.username}"
    template_local = "emails/pedido_local.html"  # nuevo template (puede ser similar al del cliente)

    html_local = render_to_string(template_local, {
        "pedido": pedido,
        "lineas_pedido": lineas_pedido,
        "nombreusuario": request.user.username,
        "total": total,
        "email_cliente": request.user.email,
        "telefono_cliente": getattr(request.user.perfilusuario, "telefono", "No informado"),
    })

    text_local = strip_tags(html_local)

    email_local = EmailMultiAlternatives(
        subject=asunto_local,
        body=text_local,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["fenrirpchardware@gmail.com"],  # <-- correo del local
    )
    email_local.attach_alternative(html_local, "text/html")
    email_local.send(fail_silently=False)


    # --- Limpiar carro y confirmar ---
    carro.limpiar_carro()
    messages.success(request, "Pedido realizado con éxito. ¡Gracias por tu compra!")

    return redirect("Tienda")
