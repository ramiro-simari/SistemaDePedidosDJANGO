def importe_total_carro(request):
    total = 0
    if request.user.is_authenticated:
        carro = request.session.get("carro", {})
        for key, value in carro.items():
            try:
                # Si el precio viene como string, convertirlo
                precio_unitario = float(value.get("precio_unitario") or value.get("precio") or 0)
                cantidad = int(value.get("cantidad", 0))
                total += precio_unitario * cantidad
            except (TypeError, ValueError):
                pass  # evita crashear si algo viene mal formateado

    # Limpiar variable temporal si existe
    if request.session.get("abrir_carrito"):
        del request.session["abrir_carrito"]

    return {"importe_total_carro": round(total, 2)}
