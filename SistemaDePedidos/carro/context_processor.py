def importe_total_carro(request):
    total = 0
    carro = request.session.get("carro", {})
    for item in carro.values():
        total += float(item["precio"])  # subtotal por producto
    return {"importe_total_carro": total}

def cantidad_total_carro(request):
    cantidad = 0
    carro = request.session.get("carro", {})
    for item in carro.values():
        cantidad += int(item.get("cantidad", 1))
    return {"cantidad_total_carro": cantidad}
