#!/bin/bash

# Development script for ProjectEvalService

set -e

echo "🚀 SICORA ProjectEvalService - Development Setup"
echo "================================================"

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo "❌ Go is not installed. Please install Go 1.23+"
    exit 1
fi

# Check Go version
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
echo "✅ Go version: $GO_VERSION"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please configure your database settings."
else
    echo "✅ .env file already exists"
fi

# Download dependencies
echo "📦 Downloading Go dependencies..."
go mod tidy

# Generate swagger docs
if command -v swag &> /dev/null; then
    echo "📚 Generating Swagger documentation..."
    swag init
else
    echo "⚠️  swag command not found. Install with: go install github.com/swaggo/swag/cmd/swag@latest"
fi

# Build the application
echo "🔨 Building application..."
go build -o projectevalservice .

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Configure your .env file with database settings"
echo "2. Ensure PostgreSQL 15 is running"
echo "3. Run the application with: ./projectevalservice"
echo "4. Access API documentation at: http://localhost:8007/swagger/index.html"
echo ""
echo "Available commands:"
echo "  go run main.go          - Run in development mode"
echo "  go test ./...           - Run tests"
echo "  go build               - Build binary"
echo "  docker build -t projectevalservice . - Build Docker image"
