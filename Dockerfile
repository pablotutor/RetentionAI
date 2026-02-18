# 1. Usamos una imagen base de Python ligera
FROM python:3.11-slim

# 2. Evitamos que Python genere archivos .pyc y forzamos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos primero los requerimientos (para aprovechar la caché de Docker)
COPY requirements.txt .

# 5. Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos TODO el resto del proyecto al contenedor
COPY . .

# 7. Exponemos el puerto de Streamlit
EXPOSE 8501

# 8. Comando para arrancar la app
# Es importante el address 0.0.0.0 para que sea visible desde fuera del contenedor
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]