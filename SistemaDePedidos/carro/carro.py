class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            carro = self.session["carro"] = {}
        self.carro = carro

    def agregar(self, producto):
        producto_id = str(producto.id)
        precio_unitario = producto.precio_oferta if getattr(producto, "precio_oferta", None) else producto.precio

        if producto_id not in self.carro.keys():
            if producto.stock > 0:
                self.carro[producto_id] = {
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    "precio_unitario": float(precio_unitario),
                    "precio": float(precio_unitario),  # subtotal inicial
                    "cantidad": 1,
                    "imagen": producto.imagen.url if producto.imagen else "",
                }
                self.guardar_carro()
                return True
            else:
                return False
        else:
            value = self.carro[producto_id]
            if value["cantidad"] < producto.stock:
                value["cantidad"] += 1
                value["precio"] = value["precio_unitario"] * value["cantidad"]
                self.guardar_carro()
                return True
            else:
                return False

    def restar_producto(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            value = self.carro[producto_id]
            value["cantidad"] -= 1
            value["precio"] = value["precio_unitario"] * value["cantidad"]
            if value["cantidad"] < 1:
                self.eliminar(producto)
            self.guardar_carro()

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            del self.carro[producto_id]
            self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True
