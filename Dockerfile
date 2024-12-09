# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias al contenedor
COPY requirements.txt requirements.txt

# Copiar el archivo de credenciales al contenedor
COPY credentials /app/credentials

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código al contenedor
COPY . .

# Configurar la variable de entorno para las credenciales
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/papyrus-technical-test-727542e11411.json

# Exponer el puerto para la aplicación
EXPOSE 8080

# Comando para ejecutar el script principal
CMD ["python", "app.py"]
