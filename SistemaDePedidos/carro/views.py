from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .carro import Carro
from tienda.models import Producto

def agregar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Producto, id=producto_id)
    
    agregado = carro.agregar(producto=producto)

    if agregado:
        messages.success(request, f"✅ {producto.nombre} agregado al carrito.")
    else:
        messages.warning(
            request,
            f"⚠️ No hay suficiente stock disponible de {producto.nombre}. "
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
    messages.info(request, "🧹 Carrito vaciado correctamente.")
    return redirect("Tienda")

def realizar_pedido(request):
    carro = Carro(request)
    productos_fuera_de_stock = []

    # Verificamos stock de cada producto en el carro
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
        # ⚠️ Si hay productos sin stock suficiente, mostramos advertencia
        mensaje = "⚠️ No se pudo realizar el pedido. Verifica los siguientes productos:\n"
        for p in productos_fuera_de_stock:
            mensaje += f"• {p['nombre']}: stock disponible {p['stock']}, en carrito {p['pedidos']}\n"

        messages.warning(request, mensaje)
        return redirect("Tienda")

    # ✅ Si hay stock suficiente, descontamos y vaciamos el carro
    for item in carro.carro.values():
        producto = Producto.objects.get(id=item["producto_id"])
        producto.stock -= item["cantidad"]
        producto.save()

    carro.limpiar_carro()
    messages.success(request, "✅ Pedido realizado con éxito. ¡Gracias por tu compra!")
    return redirect("Tienda")