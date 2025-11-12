# Imagen base con Python
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Verificar qué archivos hay (debug)
RUN ls -la

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["gunicorn", "SistemaDePedidos.wsgi:application", "--bind", "0.0.0.0:8000"]
