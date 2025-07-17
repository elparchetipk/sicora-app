#!/bin/bash

# ==============================================
# SoftwareFactoryService Development Setup
# ==============================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${BLUE}=============================================="
    echo -e "🏭 $1"
    echo -e "==============================================${NC}"
}

print_step() {
    echo -e "${CYAN}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed and running
check_docker() {
    print_step "Checking Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Docker is installed and running"
}

# Check if Docker Compose is available
check_docker_compose() {
    print_step "Checking Docker Compose..."
    
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    elif command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE="docker-compose"
    else
        print_error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi
    
    print_success "Docker Compose is available"
}

# Setup Go environment
setup_go() {
    print_step "Setting up Go environment..."
    
    if ! command -v go &> /dev/null; then
        print_warning "Go is not installed. Installing through Docker..."
    else
        print_success "Go is already installed: $(go version)"
    fi
    
    # Install Go tools if Go is available locally
    if command -v go &> /dev/null; then
        print_step "Installing Go development tools..."
        go install github.com/air-verse/air@latest
        go install github.com/swaggo/swag/cmd/swag@latest
        go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
        go install github.com/go-delve/delve/cmd/dlv@latest
        go install golang.org/x/tools/cmd/goimports@latest
        go install mvdan.cc/gofumpt@latest
        print_success "Go tools installed"
    fi
}

# Build development environment
build_dev_environment() {
    print_step "Building development environment..."
    
    # Build the development image
    docker build -f Dockerfile.dev -t sicora/softwarefactoryservice:dev .
    
    print_success "Development image built"
}

# Start development environment
start_dev_environment() {
    print_step "Starting development environment..."
    
    # Start the development environment
    $DOCKER_COMPOSE -f .devcontainer/docker-compose.dev.yml up -d
    
    # Wait for services to be ready
    print_step "Waiting for services to be ready..."
    sleep 10
    
    # Check if services are running
    if $DOCKER_COMPOSE -f .devcontainer/docker-compose.dev.yml ps | grep -q "Up"; then
        print_success "Development environment started successfully"
        
        echo -e "${PURPLE}"
        echo "🌐 Services available at:"
        echo "   - API: http://localhost:8080"
        echo "   - Swagger: http://localhost:8080/swagger/index.html"
        echo "   - PgAdmin: http://localhost:5050"
        echo "   - PostgreSQL: localhost:5432"
        echo "   - Redis: localhost:6379"
        echo -e "${NC}"
        
        echo -e "${CYAN}"
        echo "📝 Useful commands:"
        echo "   - View logs: make docker-dev-logs"
        echo "   - Access shell: make dev-shell"
        echo "   - Stop environment: make docker-dev-down"
        echo "   - Reset environment: make docker-dev-reset"
        echo -e "${NC}"
    else
        print_error "Failed to start development environment"
        $DOCKER_COMPOSE -f .devcontainer/docker-compose.dev.yml logs
        exit 1
    fi
}

# Generate Swagger documentation
generate_docs() {
    print_step "Generating Swagger documentation..."
    
    if command -v swag &> /dev/null; then
        swag init -g cmd/server/main.go -o docs/
        print_success "Swagger documentation generated"
    else
        print_warning "Swag tool not found. Documentation will be generated in container."
    fi
}

# Main setup function
main() {
    print_header "SoftwareFactoryService Development Setup"
    
    echo -e "${YELLOW}This script will set up the development environment for SoftwareFactoryService.${NC}"
    echo -e "${YELLOW}Make sure you have Docker installed and running.${NC}"
    echo ""
    
    # Ask for confirmation
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Setup cancelled"
        exit 0
    fi
    
    # Run setup steps
    check_docker
    check_docker_compose
    setup_go
    generate_docs
    build_dev_environment
    start_dev_environment
    
    print_header "Setup Complete!"
    print_success "SoftwareFactoryService development environment is ready!"
    
    echo -e "${GREEN}"
    echo "🎉 You can now start developing:"
    echo "   1. Open this folder in VS Code"
    echo "   2. Use 'Dev Containers: Reopen in Container' command"
    echo "   3. Start coding with hot reload enabled!"
    echo -e "${NC}"
}

# Handle script arguments
case "$1" in
    "clean")
        print_header "Cleaning Development Environment"
        $DOCKER_COMPOSE -f .devcontainer/docker-compose.dev.yml down -v --remove-orphans
        docker image rm sicora/softwarefactoryservice:dev 2>/dev/null || true
        print_success "Development environment cleaned"
        ;;
    "restart")
        print_header "Restarting Development Environment"
        $DOCKER_COMPOSE -f .devcontainer/docker-compose.dev.yml restart
        print_success "Development environment restarted"
        ;;
    "logs")
        print_header "Development Environment Logs"
        $DOCKER_COMPOSE -f .devcontainer/docker-compose.dev.yml logs -f
        ;;
    "status")
        print_header "Development Environment Status"
        $DOCKER_COMPOSE -f .devcontainer/docker-compose.dev.yml ps
        ;;
    *)
        main
        ;;
esac
