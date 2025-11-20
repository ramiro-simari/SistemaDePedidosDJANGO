from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum, F
from django.urls import path
from django.shortcuts import render
from .models import Pedido, LineaPedidos


# ======================================================
# INLINE DE LÍNEAS
# ======================================================
class LineaPedidosInline(admin.TabularInline):
    model = LineaPedidos
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio', 'subtotal')
    can_delete = False


# ======================================================
# ACCIONES MASIVAS
# ======================================================
def marcar_entregado(modeladmin, request, queryset):
    queryset.update(estado="entregado")
marcar_entregado.short_description = "Marcar como ENTREGADO"

def marcar_preparacion(modeladmin, request, queryset):
    queryset.update(estado="preparacion")
marcar_preparacion.short_description = "Mover a PREPARACIÓN"


# ======================================================
# ADMIN DE PEDIDOS
# ======================================================
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'estado',              # 👈 NECESARIO para list_editable
        'estado_coloreado',    # 👈 visual, no editable
        'cantidad_items',
        'fecha_facturacion',
        'mostrar_total'
    )

    list_editable = ('estado',)  # 👈 ahora sí funciona
    list_filter = ('estado', 'fecha_facturacion')
    search_fields = ('user__username', 'id')
    inlines = [LineaPedidosInline]


    actions = [marcar_entregado, marcar_preparacion]

    # -----------------------------------------
    # Colores del estado
    # -----------------------------------------
    def estado_coloreado(self, obj):
        colores = {
            'pendiente': '#f39c12',
            'preparacion': '#3498db',
            'viajando': '#9b59b6',
            'entregado': '#2ecc71',
        }
        return format_html(
            '<span style="padding:4px 10px;border-radius:6px;color:white;background:{};font-weight:bold;">{}</span>',
            colores.get(obj.estado, '#7f8c8d'),
            obj.get_estado_display()
        )
    estado_coloreado.short_description = "Estado"

    # -----------------------------------------
    # Cantidad de ítems en el pedido
    # -----------------------------------------
    def cantidad_items(self, obj):
        return obj.lineapedidos.aggregate(total=Sum('cantidad'))['total'] or 0
    cantidad_items.short_description = "Ítems"

    # -----------------------------------------
    # Formateo del total
    # -----------------------------------------
    def mostrar_total(self, obj):
        total_formateado = f"{obj.total:,.2f}"
        return format_html("<b>${}</b>", total_formateado)


    # -----------------------------------------
    # Dashboard interno (/admin/pedidos/dashboard/)
    # -----------------------------------------
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard), name="pedidos_dashboard")
        ]
        return custom_urls + urls

    def dashboard(self, request):
        data = Pedido.objects.aggregate(
            total_ingresos=Sum(F("lineapedidos__precio") * F("lineapedidos__cantidad")),
            total_pedidos=Count("id"),
        )

        pedidos_por_estado = Pedido.objects.values("estado").annotate(total=Count("id"))

        return render(request, "admin/pedidos_dashboard.html", {
            "stats": data,
            "por_estado": pedidos_por_estado
        })
