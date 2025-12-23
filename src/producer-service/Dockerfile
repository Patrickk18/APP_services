# Usamos una imagen base ligera de Python
FROM python:3.9-slim

# Evita que Python genere archivos .pyc y burocratice los logs en el buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos dependencias primero para aprovechar el caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente
COPY main.py .

# Comando de ejecución
CMD ["python", "main.py"]