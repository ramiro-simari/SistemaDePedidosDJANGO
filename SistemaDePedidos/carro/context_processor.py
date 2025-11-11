def importe_total_carro(request):
    total = 0
    if request.user.is_authenticated:
        carro = request.session.get("carro", {})
        for key, value in carro.items():
            total += float(value["precio"]) * value["cantidad"]

    # 🔹 Limpiamos la variable después de usarla (si existe)
    if request.session.get("abrir_carrito"):
        del request.session["abrir_carrito"]

    return {"importe_total_carro": total}
