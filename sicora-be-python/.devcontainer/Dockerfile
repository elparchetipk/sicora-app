FROM mcr.microsoft.com/devcontainers/python:3.13

# Instalar herramientas del sistema y configurar Python
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    postgresql-client \
    redis-tools \
    tree \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip

# Configurar directorio de trabajo
WORKDIR /workspace

# Exponer puertos para desarrollo
EXPOSE 8000 8001 8002 8003 8004 8005 8006 8007

# Variables de entorno para desarrollo
ENV PYTHONPATH=/workspace
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
