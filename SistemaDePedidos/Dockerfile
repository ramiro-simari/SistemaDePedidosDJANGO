# Imagen base
FROM python:3.11-slim

# Configuración del entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear y usar el directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos
COPY SistemaDePedidos/requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Recopilar archivos estáticos (DESPUÉS de instalar dependencias)
RUN python SistemaDePedidos/manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "SistemaDePedidos/manage.py", "runserver", "0.0.0.0:8000"]
