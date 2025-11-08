from django.db import models
from django.contrib.auth import get_user_model
from tienda.models import Producto
from django.db.models import F, Sum, FloatField
from django.utils import timezone

User = get_user_model()

# ----------------------------
# MODELO DE PEDIDO
# ----------------------------
class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('preparacion', 'En preparación'),
        ('viajando', 'Viajando'),
        ('entregado', 'Entregado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_facturacion = models.DateField(null=True, blank=True)  # 👈 clave: valor por defecto
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id}"

    @property
    def total(self):
        return self.lineas.aggregate(
            total=Sum(F("precio") * F("cantidad"), output_field=FloatField())
        )["total"] or 0

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['-created_at']



# ----------------------------
# MODELO DE LÍNEAS DE PEDIDO
# ----------------------------
class LineaPedidos(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="lineapedidos")
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lineapedidos'
        verbose_name = 'Línea de pedido'
        verbose_name_plural = 'Líneas de pedido'
        ordering = ['id']

    def __str__(self):
        if self.producto:
            return f'{self.cantidad} x {self.producto.nombre}'
        return 'Línea sin producto'

    @property
    def subtotal(self):
        return self.cantidad * self.precio
