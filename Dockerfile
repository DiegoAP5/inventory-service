# Usar una imagen base oficial de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos requirements.txt primero (para aprovechar la caché de Docker)
COPY src/requeriments.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r src/requeriments.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que tu aplicación estará corriendo (si es necesario)
EXPOSE 5000

# Comando para ejecutar tu aplicación
CMD ["python", "src/main.py"]
