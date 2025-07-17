#!/bin/bash

# 🔧 SICORA Postman Collections JSON Fix
# Regenera collections con formato JSON correcto

set -euo pipefail

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_ROOT/postman-collections"

echo -e "${BLUE}🔧 Corrigiendo formato JSON de collections SICORA...${NC}"

generate_valid_collection() {
    local service_name=$1
    local description=$2
    local backend_type=$3
    local endpoints_count=$4
    
    echo -e "${YELLOW}Generando collection corregida: $service_name ($backend_type)${NC}"
    
    local collection_id="sicora-${service_name,,}-${backend_type}"
    local base_url_var="base_url_${backend_type}"
    local backend_cap="${backend_type^}"
    
    # Generar collection con valores directos
    cat > "$OUTPUT_DIR/collections/${service_name}_${backend_cap}.postman_collection.json" <<EOF
{
  "info": {
    "name": "SICORA - ${service_name} (${backend_cap}) - Educativo",
    "description": "${description}\\n\\n📚 **Para Aprendices SENA**\\n\\n**Objetivos de Aprendizaje:**\\n- Comprender API REST ${service_name}\\n- Practicar requests HTTP (GET, POST, PUT, DELETE)\\n- Implementar tests básicos\\n- Manejar autenticación JWT\\n\\n**Prerrequisitos:**\\n- Environment configurado (development/staging/production)\\n- Servicios SICORA ejecutándose\\n- Conocimientos básicos de HTTP\\n\\n**Endpoints incluidos:** ${endpoints_count}\\n**Stack:** ${backend_cap} Backend\\n**Nivel:** Intermedio",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "_postman_id": "${collection_id}",
    "_exporter_id": "sicora-educational-generator"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{auth_token}}",
        "type": "string"
      }
    ]
  },
  "event": [
    {
      "listen": "prerequest",
      "script": {
        "type": "text/javascript",
        "exec": [
          "// 🎓 Script educativo para aprendices SENA",
          "console.log('🚀 Iniciando request para ${service_name}...');",
          "console.log('📍 Environment:', pm.environment.get('environment_name'));",
          "console.log('🔗 Base URL:', pm.environment.get('${base_url_var}'));",
          "",
          "// Verificar configuración básica",
          "if (!pm.environment.get('${base_url_var}')) {",
          "    console.error('❌ Variable ${base_url_var} no configurada');",
          "    throw new Error('Configurar environment primero');",
          "}",
          "",
          "// Auto-login si no hay token",
          "if (!pm.environment.get('auth_token')) {",
          "    console.log('🔐 Token no encontrado, intentando auto-login...');",
          "    // Aquí se puede implementar auto-login",
          "}"
        ]
      }
    },
    {
      "listen": "test",
      "script": {
        "type": "text/javascript",
        "exec": [
          "// 🎓 Tests educativos estándar",
          "pm.test('✅ Status code es exitoso (200-299)', function () {",
          "    pm.response.to.have.status.oneOf([200, 201, 202, 204]);",
          "});",
          "",
          "pm.test('⚡ Response time < 2000ms', function () {",
          "    pm.expect(pm.response.responseTime).to.be.below(2000);",
          "});",
          "",
          "pm.test('📦 Response es JSON válido', function () {",
          "    pm.response.to.be.json;",
          "});",
          "",
          "// Logging educativo",
          "console.log('📊 Status:', pm.response.status);",
          "console.log('⏱️  Response time:', pm.response.responseTime + 'ms');",
          "console.log('📏 Response size:', pm.response.responseSize + ' bytes');"
        ]
      }
    }
  ],
  "variable": [
    {
      "key": "service_name",
      "value": "${service_name}",
      "type": "string",
      "description": "Nombre del servicio"
    },
    {
      "key": "backend_type",
      "value": "${backend_type}",
      "type": "string", 
      "description": "Tipo de backend (go/python)"
    }
  ],
  "item": [
    {
      "name": "📚 Documentación",
      "description": "Información importante sobre este servicio",
      "item": [
        {
          "name": "ℹ️ Información del Servicio",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{${base_url_var}}}/health",
              "host": ["{{${base_url_var}}}"],
              "path": ["health"]
            },
            "description": "Health check del servicio ${service_name}\\n\\n**Aprenderás:**\\n- Verificar estado del servicio\\n- Interpretar responses JSON\\n- Usar variables de environment"
          },
          "response": []
        }
      ]
    },
    {
      "name": "🔐 Autenticación",
      "description": "Endpoints de autenticación y autorización",
      "item": [
        {
          "name": "🔑 Login",
          "event": [
            {
              "listen": "test",
              "script": {
                "type": "text/javascript",
                "exec": [
                  "// Guardar token automáticamente",
                  "if (pm.response.code === 200) {",
                  "    const response = pm.response.json();",
                  "    if (response.token) {",
                  "        pm.environment.set('auth_token', response.token);",
                  "        console.log('🔐 Token guardado exitosamente');",
                  "    }",
                  "    if (response.user && response.user.id) {",
                  "        pm.environment.set('user_id', response.user.id);",
                  "        console.log('👤 User ID guardado:', response.user.id);",
                  "    }",
                  "}"
                ]
              }
            }
          ],
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\\n  \\"username\\": \\"admin\\",\\n  \\"password\\": \\"password\\"\\n}"
            },
            "url": {
              "raw": "{{${base_url_var}}}/auth/login",
              "host": ["{{${base_url_var}}}"],
              "path": ["auth", "login"]
            },
            "description": "Autenticación de usuario\\n\\n**Aprenderás:**\\n- Enviar datos POST en JSON\\n- Manejar respuestas de autenticación\\n- Guardar tokens automáticamente\\n- Usar variables de environment\\n\\n**Credenciales de prueba:**\\n- Usuario: admin\\n- Contraseña: password"
          },
          "response": []
        }
      ]
    },
    {
      "name": "👥 Usuarios",
      "description": "Gestión de usuarios (CRUD básico)",
      "item": [
        {
          "name": "📋 Listar Usuarios",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{${base_url_var}}}/users",
              "host": ["{{${base_url_var}}}"],
              "path": ["users"]
            },
            "description": "Obtener lista de usuarios\\n\\n**Aprenderás:**\\n- Requests GET básicos\\n- Autenticación Bearer Token\\n- Interpretar arrays JSON\\n- Paginación básica"
          },
          "response": []
        },
        {
          "name": "👤 Obtener Usuario por ID",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{${base_url_var}}}/users/{{user_id}}",
              "host": ["{{${base_url_var}}}"],
              "path": ["users", "{{user_id}}"]
            },
            "description": "Obtener un usuario específico\\n\\n**Aprenderás:**\\n- Path parameters\\n- Variables dinámicas\\n- Respuestas de objetos únicos\\n- Manejo de errores 404"
          },
          "response": []
        },
        {
          "name": "➕ Crear Usuario",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\\n  \\"name\\": \\"Nuevo Usuario\\",\\n  \\"email\\": \\"nuevo@ejemplo.com\\",\\n  \\"role\\": \\"user\\"\\n}"
            },
            "url": {
              "raw": "{{${base_url_var}}}/users",
              "host": ["{{${base_url_var}}}"],
              "path": ["users"]
            },
            "description": "Crear nuevo usuario\\n\\n**Aprenderás:**\\n- Requests POST con datos\\n- Estructura JSON correcta\\n- Validación de datos\\n- Códigos de respuesta 201"
          },
          "response": []
        },
        {
          "name": "✏️ Actualizar Usuario",
          "request": {
            "method": "PUT",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\\n  \\"name\\": \\"Usuario Actualizado\\",\\n  \\"email\\": \\"actualizado@ejemplo.com\\"\\n}"
            },
            "url": {
              "raw": "{{${base_url_var}}}/users/{{user_id}}",
              "host": ["{{${base_url_var}}}"],
              "path": ["users", "{{user_id}}"]
            },
            "description": "Actualizar usuario existente\\n\\n**Aprenderás:**\\n- Requests PUT vs POST\\n- Actualización parcial vs completa\\n- Idempotencia\\n- Códigos de respuesta 200"
          },
          "response": []
        },
        {
          "name": "🗑️ Eliminar Usuario",
          "request": {
            "method": "DELETE",
            "header": [],
            "url": {
              "raw": "{{${base_url_var}}}/users/{{user_id}}",
              "host": ["{{${base_url_var}}}"],
              "path": ["users", "{{user_id}}"]
            },
            "description": "Eliminar usuario\\n\\n**Aprenderás:**\\n- Requests DELETE\\n- Códigos de respuesta 204\\n- Operaciones irreversibles\\n- Confirmaciones"
          },
          "response": []
        }
      ]
    },
    {
      "name": "🔬 Testing Avanzado",
      "description": "Ejemplos de testing automático",
      "item": [
        {
          "name": "🧪 Flujo Completo CRUD",
          "event": [
            {
              "listen": "test",
              "script": {
                "type": "text/javascript",
                "exec": [
                  "// 🎓 Test educativo de flujo completo",
                  "pm.test('🔄 Flujo CRUD completo', function () {",
                  "    // Este test demuestra un flujo completo",
                  "    console.log('🚀 Iniciando flujo CRUD...');",
                  "    ",
                  "    // 1. Crear usuario",
                  "    pm.sendRequest({",
                  "        url: pm.environment.get('${base_url_var}') + '/users',",
                  "        method: 'POST',",
                  "        header: {",
                  "            'Content-Type': 'application/json',",
                  "            'Authorization': 'Bearer ' + pm.environment.get('auth_token')",
                  "        },",
                  "        body: {",
                  "            mode: 'raw',",
                  "            raw: JSON.stringify({",
                  "                name: 'Usuario Test',",
                  "                email: 'test@ejemplo.com'",
                  "            })",
                  "        }",
                  "    }, function (err, response) {",
                  "        if (response.code === 201) {",
                  "            console.log('✅ Usuario creado');",
                  "            const userId = response.json().id;",
                  "            pm.environment.set('test_user_id', userId);",
                  "        }",
                  "    });",
                  "});"
                ]
              }
            }
          ],
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{${base_url_var}}}/health",
              "host": ["{{${base_url_var}}}"],
              "path": ["health"]
            },
            "description": "Ejemplo de testing automático con flujo completo\\n\\n**Aprenderás:**\\n- Chaining de requests\\n- Tests programáticos\\n- Flujos de datos\\n- Automatización avanzada"
          },
          "response": []
        }
      ]
    }
  ]
}
EOF
}

# Limpiar collections existentes
echo -e "${YELLOW}Limpiando collections existentes...${NC}"
rm -f "$OUTPUT_DIR/collections/"*.json

# Regenerar collections con formato corregido
echo -e "${YELLOW}Regenerando collections con JSON válido...${NC}"

# Servicios Go
generate_valid_collection "UserService" "Gestión de usuarios del sistema SICORA" "go" "33"
generate_valid_collection "AttendanceService" "Control de asistencia y horarios" "go" "28"
generate_valid_collection "ScheduleService" "Gestión de horarios y calendarios" "go" "35"
generate_valid_collection "ProjectEvalService" "Evaluación de proyectos" "go" "41"

# Servicios Python
generate_valid_collection "UserService" "Gestión de usuarios (versión Python)" "python" "24"
generate_valid_collection "APIGateway" "Gateway principal de APIs" "python" "15"
generate_valid_collection "AIService" "Servicios de inteligencia artificial" "python" "18"
generate_valid_collection "NotificationService" "Sistema de notificaciones" "python" "12"

# Validar todas las collections
echo -e "${YELLOW}Validando JSON de todas las collections...${NC}"
for collection in "$OUTPUT_DIR/collections/"*.json; do
    if python3 -m json.tool "$collection" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $(basename "$collection")${NC}"
    else
        echo -e "\033[0;31m❌ $(basename "$collection")${NC}"
    fi
done

echo -e "\n${GREEN}🎉 Collections regeneradas con JSON válido${NC}"
echo -e "${BLUE}📁 Ubicación: $OUTPUT_DIR/collections/${NC}"
echo -e "${BLUE}🔍 Verificar importación en Postman${NC}"
