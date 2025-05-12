# Usa una imagen base de Ubuntu
FROM ubuntu:20.04

# Configurar tzdata de forma no interactiva
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/Bogota /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Actualiza los paquetes e instala dependencias necesarias
RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://mirror.fcix.net/ubuntu/|g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    octave \
    && apt-get clean

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Establece la variable de entorno PYTHONPATH
ENV PYTHONPATH=/app

# Instala las dependencias de Python
RUN pip3 install -r requirements.txt

# Expone el puerto para Flask
EXPOSE 5000

# Comando para ejecutar el servidor Flask
CMD ["python3", "backend/run.py"]