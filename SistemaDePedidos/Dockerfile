FROM python:3.11-slim

WORKDIR /app

# Copiar todo el proyecto
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer el puerto 8000
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "SistemaDePedidos.wsgi:application", "--bind", "0.0.0.0:8000"]
