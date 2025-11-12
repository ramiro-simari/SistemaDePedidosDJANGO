# Imagen base con Python
FROM python:3.11

# Configurar directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Recolectar archivos estáticos
RUN python SistemaDePedidos/manage.py collectstatic --noinput

# Exponer el puerto (Railway usa la variable $PORT)
EXPOSE 8000

# Comando de inicio
CMD ["python", "SistemaDePedidos/manage.py", "runserver", "0.0.0.0:8000"]
