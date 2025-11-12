# Imagen base con Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el contenido del proyecto Django
COPY SistemaDePedidos/ .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput


# Comando para ejecutar con Gunicorn
CMD ["gunicorn", "SistemaDePedidos.wsgi:application", "--bind", "0.0.0.0:8000"]
