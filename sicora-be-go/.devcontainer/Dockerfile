FROM mcr.microsoft.com/devcontainers/go:1.21

# Instalar herramientas adicionales y Go tools
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/* \
    && go install github.com/swaggo/swag/cmd/swag@latest \
    && go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Configurar directorios de trabajo
WORKDIR /workspace

# Exponer puertos para desarrollo
EXPOSE 8001 8002 8003 8004 8007
