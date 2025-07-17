#!/bin/bash

# Script de verificación de versiones de Go en todo el stack SICORA
# Fecha: 29 de junio de 2025

echo "🔍 VERIFICACIÓN DE VERSIONES DE GO - STACK SICORA"
echo "=================================================="
echo

# Verificar versión instalada del sistema
echo "📊 Versión de Go instalada en el sistema:"
go version
echo

# Función para verificar cada servicio
verify_service() {
    local service_path=$1
    local service_name=$(basename $service_path)
    
    if [ -f "$service_path/go.mod" ]; then
        echo "🔸 $service_name:"
        cd "$service_path"
        
        # Extraer versión de go.mod
        local go_version=$(grep "^go " go.mod | awk '{print $2}')
        local toolchain=$(grep "^toolchain " go.mod | awk '{print $2}' 2>/dev/null)
        
        echo "   ├─ Versión Go: $go_version"
        if [ ! -z "$toolchain" ]; then
            echo "   ├─ Toolchain: $toolchain"
        else
            echo "   ├─ Toolchain: (no especificado)"
        fi
        
        # Verificar compilación
        echo "   └─ Compilación:"
        if [ -d "cmd/server" ]; then
            if go build ./cmd/server 2>/dev/null; then
                echo "      ✅ Compila correctamente"
                rm -f server 2>/dev/null
            else
                echo "      ❌ Error de compilación"
            fi
        elif [ -f "main.go" ]; then
            if go build . 2>/dev/null; then
                echo "      ✅ Compila correctamente"
                rm -f $service_name 2>/dev/null
            else
                echo "      ❌ Error de compilación"
            fi
        else
            echo "      ⚠️  No se encontró punto de entrada"
        fi
        echo
    else
        echo "🔸 $service_name: ❌ Sin go.mod"
        echo
    fi
}

# Base path
BASE_PATH="/home/epti/Documentos/epti-dev/sicora-app/sicora-be-go"

echo "🏗️  SERVICIOS DEL STACK:"
echo "======================="

# Verificar módulo raíz
echo "🔸 sicora-be-go (raíz):"
cd "$BASE_PATH"
go_version=$(grep "^go " go.mod | awk '{print $2}')
toolchain=$(grep "^toolchain " go.mod | awk '{print $2}' 2>/dev/null)
echo "   ├─ Versión Go: $go_version"
if [ ! -z "$toolchain" ]; then
    echo "   ├─ Toolchain: $toolchain"
else
    echo "   ├─ Toolchain: (no especificado)"
fi
echo "   └─ Estado: Módulo de coordinación"
echo

# Lista de servicios
services=(
    "userservice"
    "mevalservice"
    "scheduleservice"
    "attendanceservice"
    "evalinservice"
    "projectevalservice"
)

# Verificar cada servicio
for service in "${services[@]}"; do
    verify_service "$BASE_PATH/$service"
done

echo "📋 RESUMEN:"
echo "==========="

# Verificar consistencia
echo "🎯 Verificando consistencia de versiones..."

consistent=true
expected_go="1.23"
expected_toolchain="go1.24.4"

for service in "${services[@]}"; do
    service_path="$BASE_PATH/$service"
    if [ -f "$service_path/go.mod" ]; then
        cd "$service_path"
        go_version=$(grep "^go " go.mod | awk '{print $2}')
        toolchain=$(grep "^toolchain " go.mod | awk '{print $2}' 2>/dev/null)
        
        if [ "$go_version" != "$expected_go" ]; then
            echo "   ❌ $service: Go $go_version (esperado: $expected_go)"
            consistent=false
        fi
        
        if [ ! -z "$toolchain" ] && [ "$toolchain" != "$expected_toolchain" ]; then
            echo "   ❌ $service: Toolchain $toolchain (esperado: $expected_toolchain)"
            consistent=false
        fi
    fi
done

if [ "$consistent" = true ]; then
    echo "   ✅ Todas las versiones son consistentes"
    echo "   📌 Estándar: Go $expected_go con toolchain $expected_toolchain"
else
    echo "   ⚠️  Se encontraron inconsistencias"
fi

echo
echo "🚀 RECOMENDACIONES:"
echo "==================="
echo "✅ Versión LTS recomendada: Go 1.23"
echo "✅ Toolchain actual: go1.24.4"
echo "📚 Para actualizar un servicio:"
echo "   - Editar go.mod: 'go 1.23'"
echo "   - Agregar toolchain: 'toolchain go1.24.4'"
echo "   - Ejecutar: 'go mod tidy'"
echo

echo "✨ Verificación completada - $(date)"
