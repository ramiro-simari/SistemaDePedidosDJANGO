from django.db import models

# Create your models here.

class CategoriaProd(models.Model):
    nombre=models.CharField(max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="categoriaProd"
        verbose_name_plural="categoriasProd"
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    categorias = models.ForeignKey(CategoriaProd, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="tienda", null=True, blank=True)
    precio = models.FloatField()
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio en oferta")
    stock = models.PositiveIntegerField(default=0)
    disponibilidad = models.BooleanField(default=True)
    en_oferta = models.BooleanField(default=False, verbose_name="¿Está en oferta?")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre
    
    def get_precio_final(self):
        """Devuelve el precio con o sin oferta."""
        if self.en_oferta and self.precio_oferta:
            return self.precio_oferta
        return self.precio
