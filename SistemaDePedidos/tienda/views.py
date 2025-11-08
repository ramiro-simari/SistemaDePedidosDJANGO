from django.shortcuts import render, get_object_or_404
from .models import Producto, CategoriaProd

def tienda(request, categoria_id=None):
    categorias = CategoriaProd.objects.all()
    productos = Producto.objects.all()
    categoria_seleccionada = None

    # Filtro por categoría (si viene en la URL)
    if categoria_id:
        categoria_seleccionada = get_object_or_404(CategoriaProd, id=categoria_id)
        productos = productos.filter(categorias=categoria_seleccionada)

    # Filtro por búsqueda (si viene en el GET)
    query = request.GET.get("q")
    if query:
        productos = productos.filter(nombre__icontains=query)

    contexto = {
        "productos": productos.distinct(),
        "categorias": categorias,
        "categoria_seleccionada": categoria_seleccionada,
        "query": query or "",
    }
    return render(request, "tienda/tienda.html", contexto)
