from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, F
from .models import Pedido, LineaPedidos


# Inline para mostrar las líneas dentro del pedido
class LineaPedidoInline(admin.TabularInline):
    model = LineaPedidos
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio', 'subtotal')
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'mostrar_total', 'estado_coloreado', 'estado')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__username', 'usuario__email')
    list_editable = ('estado',)
    readonly_fields = ('usuario', 'fecha_pedido', 'mostrar_total')
    inlines = [LineaPedidoInline]
    ordering = ('-fecha_pedido',)

    # --------- Mostrar total calculado ----------
    def mostrar_total(self, obj):
        total = obj.lineas.aggregate(
            total=Sum(F('precio') * F('cantidad'))
        )['total'] or 0
        return f"${total:,.2f}"
    mostrar_total.short_description = "Total"

    # --------- Mostrar estado con color ----------
    def estado_coloreado(self, obj):
        colores = {
            'PENDIENTE': ("#faaa15", 'Pendiente'),
            'EN_PREPARACION': ('#a855f7', 'En preparación'),
            'VIAJANDO': ('#3b82f6', 'Viajando'),
            'ENTREGADO': ('#22c55e', 'Entregado'),
        }
        color, label = colores.get(obj.estado, ('#9ca3af', obj.estado))
        return format_html(
            '<span style="background-color:{}; color:white; padding:4px 8px; border-radius:6px; font-weight:bold;">{}</span>',
            color, label
        )
    estado_coloreado.short_description = "Estado actual"

    # Evitar que Django lo interprete como editable por error
    estado_coloreado.allow_tags = True


@admin.register(LineaPedidos)
class LineaPedidosAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio', 'subtotal')
    search_fields = ('producto__nombre',)
