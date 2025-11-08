from django.contrib import admin
from django.utils.html import format_html
from .models import CategoriaProd, Producto


@admin.register(CategoriaProd)
class CategoriaProdAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    list_display = ("nombre", "created")
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    list_display = (
        "nombre",
        "categorias",
        "precio",
        "stock",             # editable
        "colored_stock",     # visual con color
        "disponibilidad",
    )
    list_editable = ("precio", "disponibilidad", "stock")
    list_filter = ("categorias", "disponibilidad")
    search_fields = ("nombre",)
    ordering = ("categorias", "nombre")

    # --- Método visual del stock ---
    def colored_stock(self, obj):
        """Muestra el stock con color según la cantidad."""
        if obj.stock == 0:
            color = "red"
            text = "Sin stock"
        elif obj.stock < 5:
            color = "orange"
            text = f"{obj.stock} (bajo)"
        elif obj.stock < 15:
            color = "gold"
            text = f"{obj.stock}"
        else:
            color = "limegreen"
            text = f"{obj.stock}"

        return format_html('<strong style="color:{};">{}</strong>', color, text)

    colored_stock.short_description = "Stock (visual)"
