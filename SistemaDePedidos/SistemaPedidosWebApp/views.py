from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    return render(request, "SistemaPedidosWebApp/home.html")

def tienda(request):
    return render(request, "SistemaPedidosWebApp/tienda.html")

def blog(request):
    return render(request, "SistemaPedidosWebApp/blog.html")

def contacto(request):
    return render(request, "SistemaPedidosWebApp/contacto.html")