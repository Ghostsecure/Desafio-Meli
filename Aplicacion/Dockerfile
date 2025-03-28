#Imagen base para nuestro contenedor, Python slim como base.
FROM python:3.9-slim

#Directorio de trabajo en nuestro contenedor
WORKDIR /app

# Instalación de dependencias del sistema: paquetes, compilador de C que es gcc, la biblioteca para conectar a mysql y eliminacion de archivos temporales 
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer variables de entorno para la compilación, el primero nos sirve para que Python no genere archivos .pyc, el segundo desactiva el almacenamiento en el 
#buffer, lo que permite mostrar en tiempo real  los logs y los mensajes.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar requirements y instalar dependencias, evitando que se guarde en la caché local
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorio para los datos
RUN mkdir -p /data

# Copiar el código de la aplicación a esta direccion dentro de esta direccion
COPY ./app /app

# Crear un usuario no root para la aplicación, lo que permite leer y escribir
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app /data

# Cambiar al usuario no root, con la intencion de que el comando siguiente sea ejecutado con este usuario
USER appuser

# Comando para ejecutar la aplicación de inicializacion
COPY ./app /app
COPY --chmod=0755 ./app/start.sh /app/
CMD ["/bin/bash", "/app/start.sh"]