FROM python:3.11-slim

WORKDIR /app

# Copiar todo al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "SistemaDePedidos.wsgi:application", "--bind", "0.0.0.0:8000"]
