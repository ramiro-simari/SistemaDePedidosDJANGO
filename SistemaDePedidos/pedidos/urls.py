from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path('', views.procesar_pedido, name="procesar_pedido"),
    path('mis-pedidos/', views.mis_pedidos, name="mis_pedidos"),
    path('detalle/<int:pedido_id>/', views.detalle_pedido, name="detalle_pedido"),
]
