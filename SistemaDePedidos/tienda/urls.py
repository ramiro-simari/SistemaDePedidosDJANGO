from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name="Tienda"),
    path('categoria/<int:categoria_id>/', views.tienda, name="productos_por_categoria"),
]