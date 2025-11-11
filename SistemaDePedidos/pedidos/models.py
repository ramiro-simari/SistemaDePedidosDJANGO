from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F, Sum, FloatField
from tienda.models import Producto

User = get_user_model()


# ----------------------------
# MODELO DE PEDIDO
# ----------------------------
class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PREPARACION', 'En preparación'),
        ('VIAJANDO', 'Viajando'),
        ('ENTREGADO', 'Entregado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username} ({self.get_estado_display()})"

    @property
    def total(self):
        """Calcula el total sumando todas las líneas de pedido."""
        return self.lineas.aggregate(
            total=Sum(F("precio") * F("cantidad"), output_field=FloatField())
        )["total"] or 0
    


# ----------------------------
# MODELO DE LÍNEAS DE PEDIDO
# ----------------------------
class LineaPedidos(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="lineas"
    )
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
            return f"{self.cantidad} x {self.producto.nombre}"
        return f"Línea de pedido #{self.id} (sin producto)"

    @property
    def subtotal(self):
        return self.cantidad * self.precio
