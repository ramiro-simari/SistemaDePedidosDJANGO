from django.urls import path
from . import views

urlpatterns = [
    #path('', views.procesar_pedido, name="realizar_pedido"),
    path("historial/", views.historial_pedidos, name="historial_pedidos"),
]