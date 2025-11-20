from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pedidos.models import LineaPedidos, Pedido
from carro.carro import Carro
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

@login_required(login_url="/autenticacion/logear")
def procesar_pedido(request):
    carro = Carro(request)

    if not carro.carro:
        messages.warning(request, "Tu carrito está vacío")
        return redirect("Tienda")

    # Crear pedido
    pedido = Pedido.objects.create(user=request.user)

    lineas_pedido = []
    for key, value in carro.carro.items():
        lineas_pedido.append(
            LineaPedidos(
                pedido=pedido,
                producto_id=value["producto_id"],
                cantidad=value["cantidad"],
                precio=value["precio_unitario"]
            )
        )

    LineaPedidos.objects.bulk_create(lineas_pedido)

    # Enviar email
    enviar_mail_cliente(pedido, lineas_pedido, request.user)
    enviar_mail_tienda(pedido, lineas_pedido, request.user)

    # Vaciar carrito
    carro.limpiar_carro()

    messages.success(request, "El pedido se ha creado correctamente")
    return redirect("Tienda")


def enviar_mail_cliente(pedido, lineas_pedido, usuario):
    asunto = "Gracias por tu compra en FenrirPC"
    html = render_to_string("pedidos/emails/factura_cliente.html", {
        "pedido": pedido,
        "lineas_pedido": lineas_pedido,
        "nombre": usuario.username,
    })
    texto = strip_tags(html)

    send_mail(
        asunto,
        texto,
        "ramirosimari26@gmail.com",        # Remitente
        [usuario.email],                   # 📩 CLIENTE
        html_message=html
    )


def enviar_mail_tienda(pedido, lineas_pedido, usuario):
    asunto = f"Nuevo pedido #{pedido.id} de {usuario.username}"
    html = render_to_string("pedidos/emails/pedido_empresa.html", {
        "pedido": pedido,
        "lineas_pedido": lineas_pedido,
        "usuario": usuario,
    })
    texto = strip_tags(html)

    send_mail(
        asunto,
        texto,
        "ramirosimari26@gmail.com",        # Remitente
        ["ramirosimari.dev@gmail.com"],    # 📩 EMPRESA
        html_message=html
    )

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by('-fecha_facturacion')

    return render(request, 'pedidos/mis_pedidos.html', {
        'pedidos': pedidos
    })

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, user=request.user)
    lineas = pedido.lineapedidos.all()

    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'lineas': lineas
    })