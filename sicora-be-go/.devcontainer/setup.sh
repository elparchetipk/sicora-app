#!/bin/bash
# Script para configurar submódulos en GitHub Codespaces

echo "🔧 Configurando submódulos para SICORA..."

# Configurar Git para Codespaces
git config --global user.name "Codespace User"
git config --global user.email "user@codespace.local"

# Inicializar submódulos si existen
if [ -f ".gitmodules" ]; then
    echo "📦 Inicializando submódulos..."
    git submodule update --init --recursive
    
    # Configurar URLs para HTTPS (necesario en Codespaces)
    git submodule foreach 'git config url."https://github.com/".insteadOf git@github.com:'
else
    echo "📁 Configurando enlaces a recursos compartidos..."
    
    # Si no hay submódulos, crear enlaces simbólicos
    if [ ! -d "shared" ]; then
        echo "🔗 Clonando sicora-shared..."
        git clone https://github.com/tu-org/sicora-shared.git shared
    fi
    
    if [ ! -d "infra" ]; then
        echo "🔗 Clonando sicora-infra..."
        git clone https://github.com/tu-org/sicora-infra.git infra
    fi
fi

# Instalar dependencias específicas del stack
if [ -f "go.mod" ]; then
    echo "📦 Instalando dependencias Go..."
    go mod download
    go mod tidy
elif [ -f "requirements.txt" ]; then
    echo "🐍 Instalando dependencias Python..."
    pip install -r requirements.txt
elif [ -f "package.json" ]; then
    echo "📦 Instalando dependencias Node..."
    npm install
fi

echo "✅ Configuración de Codespace completada!"
