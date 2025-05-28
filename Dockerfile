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

RUN mkdir -p /app/backend/octave && chmod -R 755 /app/backend/octave

# Establece la variable de entorno PYTHONPATH
ENV PYTHONPATH=/app

# Instala las dependencias de Python
RUN pip3 install -r requirements.txt

# Expone los puertos para Flask y Streamlit
EXPOSE 5000 8501

# Comando para ejecutar ambos servidores (Flask y Streamlit)
CMD ["sh", "-c", "python3 run.py & streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0"]