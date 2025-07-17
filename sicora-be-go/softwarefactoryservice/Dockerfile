# Multi-stage build for optimized image size
FROM golang:1.23-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
RUN apk add --no-cache git

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/server

# Final stage
FROM alpine:latest

# Install ca-certificates for SSL verification
RUN apk --no-cache add ca-certificates tzdata

# Set timezone
ENV TZ=America/Bogota

WORKDIR /root/

# Copy binary from builder stage
COPY --from=builder /app/main .

# Copy configuration files if any
COPY --from=builder /app/.env.example .env

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["./main"]
