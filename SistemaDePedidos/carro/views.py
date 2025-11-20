from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .carro import Carro
from tienda.models import Producto
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from pedidos.models import Pedido, LineaPedidos
from django.utils import timezone



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

    return redirect("Tienda")


def eliminar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carro.eliminar(producto=producto)
    messages.info(request, f"🗑️ {producto.nombre} eliminado del carrito.")
    return redirect("Tienda")


def restar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carro.restar_producto(producto=producto)
    return redirect("Tienda")


def limpiar_carro(request):
    carro = Carro(request)
    carro.limpiar_carro()
    messages.info(request, "Carrito vaciado correctamente.")
    return redirect("Tienda")

def realizar_pedido(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para realizar un pedido.")
        return redirect("login")

    carro = Carro(request)
    productos_fuera_de_stock = []

    # Verificar stock
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
        mensaje = " No se pudo realizar el pedido. Verifica los siguientes productos:<br>"
        for p in productos_fuera_de_stock:
            mensaje += f"• {p['nombre']}: stock disponible {p['stock']}, en carrito {p['pedidos']}<br>"

        messages.warning(request, mensaje)
        return redirect("Tienda")

    # Crear pedido
    pedido = Pedido.objects.create(
        user=request.user,
        estado="pendiente",
        fecha_facturacion=timezone.now().date()
    )

    # Crear líneas de pedido + descontar stock
    for item in carro.carro.values():
        producto = Producto.objects.get(id=item["producto_id"])

        LineaPedidos.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item["cantidad"],
            precio=item["precio_unitario"],
        )

        # descontar stock
        producto.stock -= item["cantidad"]
        producto.save()

    # Datos para los emails
    lineas = pedido.lineapedidos.all()
    total_pedido = pedido.total
    cliente = request.user

    # Renderizar HTML del correo (cliente)
    html_cliente = render_to_string("pedidos/emails/factura_cliente.html", {
        "pedido": pedido,
        "lineas": lineas,
        "total": total_pedido,
        "cliente": cliente,
    })
    texto_cliente = strip_tags(html_cliente)

    # Enviar email al cliente
    send_mail(
        subject=f"Factura de tu compra - Pedido #{pedido.id}",
        message=texto_cliente,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[cliente.email],
        html_message=html_cliente,
    )

    # Renderizar correo para el local
    html_empresa = render_to_string("pedidos/emails/pedido_empresa.html", {
        "pedido": pedido,
        "lineas": lineas,
        "total": total_pedido,
        "cliente": cliente,
    })
    texto_empresa = strip_tags(html_empresa)

    # Enviar email al local
    send_mail(
        subject=f"Nuevo Pedido #{pedido.id} - Preparar pedido",
        message=texto_empresa,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["fenrirpchardware@gmail.com"],  # correo del local
        html_message=html_empresa,
    )

    # Limpiar carrito
    carro.limpiar_carro()

    messages.success(request, "Pedido realizado con éxito. Te enviamos la factura por email 😊")
    return redirect("Tienda")
