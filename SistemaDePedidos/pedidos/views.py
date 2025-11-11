from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pedidos.models import Pedido
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Pedido

@login_required(login_url="/autenticacion/logear")
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by("-fecha_pedido")
    return render(request, "pedidos/historial_pedidos.html", {"pedidos": pedidos})
