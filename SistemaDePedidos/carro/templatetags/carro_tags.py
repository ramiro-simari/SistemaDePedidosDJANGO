from django import template
from tienda.models import Producto

register = template.Library()

@register.filter
def stock_disponible(producto_id):
    """Devuelve el stock actual del producto."""
    try:
        producto = Producto.objects.get(id=producto_id)
        return producto.stock
    except Producto.DoesNotExist:
        return 0
