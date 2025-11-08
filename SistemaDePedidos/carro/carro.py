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

        # Si el producto no está en el carro
        if producto_id not in self.carro.keys():
            # Validar que haya stock
            if producto.stock > 0:
                self.carro[producto_id] = {
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    "precio": str(producto.precio),
                    "cantidad": 1,
                    "imagen": producto.imagen.url if producto.imagen else "",
                }
                self.guardar_carro()
                return True  # agregado correctamente
            else:
                return False  # sin stock disponible

        # Si el producto ya está en el carro, controlar stock
        else:
            for key, value in self.carro.items():
                if key == producto_id:
                    if value["cantidad"] < producto.stock:
                        value["cantidad"] += 1
                        value["precio"] = float(value["precio"]) + producto.precio
                        self.guardar_carro()
                        return True
                    else:
                        # Ya se alcanzó el límite de stock
                        return False

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            del self.carro[producto_id]
            self.guardar_carro()

    def restar_producto(self, producto):
        producto_id = str(producto.id)
        for key, value in self.carro.items():
            if key == producto_id:
                value["cantidad"] -= 1
                value["precio"] = float(value["precio"]) - producto.precio
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                break
        self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True
