# Imagen base con Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto (la carpeta SistemaDePedidos)
COPY SistemaDePedidos/ .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "SistemaDePedidos.wsgi:application", "--bind", "0.0.0.0:8000"]
