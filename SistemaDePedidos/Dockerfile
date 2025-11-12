# Imagen base con Python
FROM python:3.13.4

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "SistemaDePedidos.wsgi:application", "--bind", "0.0.0.0:8000"]
