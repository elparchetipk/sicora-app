# Build stage
FROM golang:1.21-alpine AS builder

# Instalar dependencias del sistema
RUN apk add --no-cache git ca-certificates tzdata

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de módulo Go
COPY go.mod go.sum ./

# Descargar dependencias
RUN go mod download

# Copiar código fuente
COPY . .

# Compilar la aplicación
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/server

# Final stage
FROM alpine:latest

# Instalar ca-certificates para HTTPS
RUN apk --no-cache add ca-certificates tzdata

# Crear usuario no privilegiado
RUN adduser -D -s /bin/sh attendanceuser

# Establecer directorio de trabajo
WORKDIR /root/

# Copiar el binario desde el stage de build
COPY --from=builder /app/main .

# Copiar archivo de configuración de ejemplo
COPY --from=builder /app/.env.example .

# Cambiar permisos
RUN chown attendanceuser:attendanceuser main
RUN chmod +x main

# Cambiar a usuario no privilegiado
USER attendanceuser

# Exponer puerto
EXPOSE 8003

# Configurar health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8003/health || exit 1

# Comando para ejecutar la aplicación
CMD ["./main"]
