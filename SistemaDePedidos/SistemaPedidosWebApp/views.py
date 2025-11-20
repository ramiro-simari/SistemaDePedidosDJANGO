from django.shortcuts import render
from tienda.models import Producto
from carro.carro import Carro

def home(request):
    carro = Carro(request)

    # Obtener productos en oferta
    productos_oferta = Producto.objects.filter(precio_oferta__gt=0, disponibilidad=True)

    context = {
        'productos_oferta': productos_oferta,
    }

    return render(request, "SistemaPedidosWebApp/home.html", context)
