from django.shortcuts import render, HttpResponse
from carro.carro import Carro
from tienda.models import Producto

# Create your views here.

def home(request):

    carro=Carro(request)
    productos_oferta = Producto.objects.filter(en_oferta=True).order_by('-id')[:10]

    return render(request, "SistemaPedidosWebApp/home.html", {
        "productos_oferta": productos_oferta
    })