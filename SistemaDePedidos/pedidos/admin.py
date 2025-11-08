from django.contrib import admin
from .models import Pedido, LineaPedidos

# ----------------------------
# INLINE para mostrar líneas dentro del pedido
# ----------------------------
class LineaPedidosInline(admin.TabularInline):
    model = LineaPedidos
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio', 'subtotal')
    can_delete = False


# ----------------------------
# ADMIN DE PEDIDO
# ----------------------------
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'estado', 'fecha_facturacion', 'mostrar_total')
    list_filter = ('estado', 'fecha_facturacion')
    readonly_fields = ('fecha_facturacion',)
    search_fields = ('user__username',)
    inlines = [LineaPedidosInline]

    def mostrar_total(self, obj):
        return f"${obj.total:,.2f}"
    mostrar_total.short_description = "Total"


# ----------------------------
# ADMIN DE LÍNEAS DE PEDIDO
# ----------------------------
@admin.register(LineaPedidos)
class LineaPedidosAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'producto', 'cantidad', 'precio', 'subtotal')
    readonly_fields = ('subtotal',)
    search_fields = ('producto__nombre', 'pedido__id')
    list_filter = ('pedido__estado',)
