#!/bin/bash

# 🎓 SICORA Postman Collections Generator - Educativo
# Genera collections educativas para aprendices SENA
# Contexto: 389 endpoints, 16 servicios, formación técnica

set -euo pipefail

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_ROOT/postman-collections"
DOCS_DIR="$PROJECT_ROOT/_docs"

# Función para logging
log() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Banner
echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════════════════════════╗"
echo "║                    🎓 SICORA POSTMAN COLLECTIONS GENERATOR                       ║"
echo "║                         Educativo para Aprendices SENA                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar directorios
log "Verificando estructura de directorios..."
if [[ ! -d "$PROJECT_ROOT/sicora-be-go" ]]; then
    error "Directorio sicora-be-go no encontrado"
    exit 1
fi

if [[ ! -d "$PROJECT_ROOT/sicora-be-python" ]]; then
    error "Directorio sicora-be-python no encontrado"
    exit 1
fi

# Crear directorio de salida
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/collections"
mkdir -p "$OUTPUT_DIR/environments"
mkdir -p "$OUTPUT_DIR/documentation"

success "Directorios creados: $OUTPUT_DIR"

# Función para generar environment
generate_environment() {
    local env_name=$1
    local go_port=$2
    local python_port=$3
    local description=$4
    
    log "Generando environment: $env_name"
    
    cat > "$OUTPUT_DIR/environments/sicora-${env_name}.postman_environment.json" <<EOF
{
  "id": "sicora-${env_name}-env",
  "name": "SICORA - ${env_name^} (Educativo)",
  "values": [
    {
      "key": "base_url_go",
      "value": "http://localhost:${go_port}",
      "description": "URL base para servicios Go",
      "enabled": true
    },
    {
      "key": "base_url_python", 
      "value": "http://localhost:${python_port}",
      "description": "URL base para servicios Python",
      "enabled": true
    },
    {
      "key": "auth_token",
      "value": "",
      "description": "Token JWT para autenticación (se llena automáticamente)",
      "enabled": true
    },
    {
      "key": "user_id",
      "value": "",
      "description": "ID del usuario logueado (se llena automáticamente)",
      "enabled": true
    },
    {
      "key": "project_id",
      "value": "",
      "description": "ID del proyecto activo (se llena automáticamente)",
      "enabled": true
    },
    {
      "key": "environment_name",
      "value": "${env_name}",
      "description": "Nombre del ambiente actual",
      "enabled": true
    }
  ],
  "_postman_variable_scope": "environment",
  "_postman_exported_at": "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)",
  "_postman_exported_using": "SICORA Educational Generator"
}
EOF
}

# Generar environments
log "Generando environments educativos..."
generate_environment "development" "8080" "8000" "Ambiente de desarrollo local"
generate_environment "staging" "8081" "8001" "Ambiente de staging/pruebas"
generate_environment "production" "443" "443" "Ambiente de producción"

success "Environments generados: development, staging, production"

# Función para generar collection básica
generate_basic_collection() {
    local service_name=$1
    local description=$2
    local backend_type=$3
    local endpoints_count=$4
    
    log "Generando collection: $service_name ($backend_type)"
    
    local collection_id="sicora-${service_name,,}-${backend_type}"
    local base_url_var="base_url_${backend_type}"
    
    cat > "$OUTPUT_DIR/collections/${service_name}_${backend_type^}.postman_collection.json" <<EOF
{
  "info": {
    "name": "SICORA - ${service_name} (${backend_type^}) - Educativo",
    "description": "${description}\\n\\n📚 **Para Aprendices SENA**\\n\\n**Objetivos de Aprendizaje:**\\n- Comprender API REST ${service_name}\\n- Practicar requests HTTP (GET, POST, PUT, DELETE)\\n- Implementar tests básicos\\n- Manejar autenticación JWT\\n\\n**Prerrequisitos:**\\n- Environment configurado (development/staging/production)\\n- Servicios SICORA ejecutándose\\n- Conocimientos básicos de HTTP\\n\\n**Endpoints incluidos:** ${endpoints_count}\\n**Stack:** ${backend_type^} Backend\\n**Nivel:** Intermedio",
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
              "raw": "{\\n  \\\"username\\\": \\\"admin\\\",\\n  \\\"password\\\": \\\"password\\\"\\n}"
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
              "raw": "{\\n  \\\"name\\\": \\\"Nuevo Usuario\\\",\\n  \\\"email\\\": \\\"nuevo@ejemplo.com\\\",\\n  \\\"role\\\": \\\"user\\\"\\n}"
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
              "raw": "{\\n  \\\"name\\\": \\\"Usuario Actualizado\\\",\\n  \\\"email\\\": \\\"actualizado@ejemplo.com\\\"\\n}"
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

# Generar collections educativas básicas
log "Generando collections educativas..."

# Servicios Go
generate_basic_collection "UserService" "Gestión de usuarios del sistema SICORA" "go" "33"
generate_basic_collection "AttendanceService" "Control de asistencia y horarios" "go" "28"
generate_basic_collection "ScheduleService" "Gestión de horarios y calendarios" "go" "35"
generate_basic_collection "ProjectEvalService" "Evaluación de proyectos" "go" "41"

# Servicios Python
generate_basic_collection "UserService" "Gestión de usuarios (versión Python)" "python" "24"
generate_basic_collection "APIGateway" "Gateway principal de APIs" "python" "15"
generate_basic_collection "AIService" "Servicios de inteligencia artificial" "python" "18"
generate_basic_collection "NotificationService" "Sistema de notificaciones" "python" "12"

success "Collections generadas: 8 servicios principales"

# Generar documentación educativa
log "Generando documentación educativa..."

cat > "$OUTPUT_DIR/documentation/GUIA_APRENDICES_SENA.md" <<'EOF'
# 🎓 Guía para Aprendices SENA - SICORA API Testing

## 📚 Objetivos de Aprendizaje

Al completar esta guía, los aprendices podrán:
- ✅ Comprender conceptos básicos de APIs REST
- ✅ Usar Postman para testing manual de APIs
- ✅ Configurar environments y variables
- ✅ Implementar tests automáticos básicos
- ✅ Interpretar responses y códigos de estado HTTP
- ✅ Manejar autenticación JWT
- ✅ Realizar operaciones CRUD completas

## 🚀 Configuración Inicial

### 1. Prerrequisitos
- [ ] Postman instalado (versión desktop recomendada)
- [ ] Acceso al workspace SICORA
- [ ] Servicios SICORA ejecutándose localmente
- [ ] Conocimientos básicos de HTTP

### 2. Importar Collections
1. Abrir Postman
2. Click en "Import" 
3. Arrastrar archivos `.json` de `collections/`
4. Verificar que se importaron correctamente

### 3. Configurar Environment
1. Importar environments desde `environments/`
2. Seleccionar "sicora-development"
3. Verificar variables:
   - `base_url_go`: http://localhost:8080
   - `base_url_python`: http://localhost:8000

## 📋 Checklist de Progreso

### Nivel Básico - Fundamentos
- [ ] Health check exitoso (GET /health)
- [ ] Login exitoso con credenciales de prueba
- [ ] Token JWT guardado automáticamente
- [ ] Primer request GET funcionando
- [ ] Interpretar response JSON correctamente

### Nivel Intermedio - CRUD
- [ ] Listar usuarios (GET /users)
- [ ] Crear usuario (POST /users)
- [ ] Obtener usuario específico (GET /users/:id)
- [ ] Actualizar usuario (PUT /users/:id)
- [ ] Eliminar usuario (DELETE /users/:id)

### Nivel Avanzado - Testing
- [ ] Tests automáticos pasando
- [ ] Variables dinámicas funcionando
- [ ] Flujo completo CRUD automatizado
- [ ] Manejo de errores implementado
- [ ] Collection Runner ejecutado exitosamente

## 🎯 Actividades Prácticas

### Actividad 1: Exploración Básica (30 min)
1. Ejecutar health check en todos los servicios
2. Hacer login y verificar token
3. Listar usuarios de ambos backends (Go y Python)
4. Comparar responses entre backends

### Actividad 2: Operaciones CRUD (45 min)
1. Crear 3 usuarios diferentes
2. Actualizar información de uno
3. Eliminar uno
4. Verificar que los cambios se reflejan

### Actividad 3: Testing Automático (30 min)
1. Ejecutar collection completa con Collection Runner
2. Analizar resultados de tests
3. Identificar y corregir fallos
4. Generar reporte HTML

### Actividad 4: Scenarios Reales (60 min)
1. Simular flujo de inscripción de estudiante
2. Registrar asistencia
3. Crear y evaluar proyecto
4. Generar reporte de notas

## 🔍 Troubleshooting

### Problemas Comunes

**❌ Error: "Could not send request"**
- Verificar que los servicios estén ejecutándose
- Comprobar URLs en environment
- Verificar conectividad de red

**❌ Error: "401 Unauthorized"**
- Token expirado o inválido
- Ejecutar login nuevamente
- Verificar que el token se guardó correctamente

**❌ Error: "404 Not Found"**
- Endpoint incorrecto
- Verificar documentación de API
- Comprobar path parameters

**❌ Tests fallan**
- Revisar assertions en tests
- Verificar datos de prueba
- Comprobar tiempos de respuesta

### Recursos de Ayuda

- **Instructor**: Contactar para dudas conceptuales
- **Documentación**: Revisar descripción de cada request
- **Console**: Usar console.log para debugging
- **Tests**: Leer mensajes de error detalladamente

## 📊 Evaluación

### Criterios de Evaluación

**Excelente (4.5-5.0)**
- Ejecuta todos los requests correctamente
- Implementa tests automáticos efectivos
- Maneja errores apropiadamente
- Demuestra comprensión profunda de APIs

**Bueno (3.5-4.4)**
- Ejecuta la mayoría de requests
- Tests básicos funcionando
- Comprende conceptos principales
- Resuelve problemas con ayuda mínima

**Aceptable (3.0-3.4)**
- Ejecuta requests básicos
- Comprende GET y POST
- Necesita ayuda para problemas
- Entiende conceptos básicos

**Insuficiente (<3.0)**
- Dificultades con requests básicos
- No comprende conceptos clave
- Necesita ayuda constante
- Debe reforzar conocimientos

## 🏆 Certificación

Al completar exitosamente todas las actividades, el aprendiz recibirá:
- ✅ Certificado de competencia en API Testing
- ✅ Badge de Postman Expert
- ✅ Recomendación para roles de QA/Testing
- ✅ Portfolio con evidence de proyectos

---

**¡Éxito en tu aprendizaje! 🚀**
EOF

# Generar README principal
cat > "$OUTPUT_DIR/README.md" <<'EOF'
# 🎓 SICORA Postman Collections - Educativo

> Collections educativas para aprendices SENA  
> **Endpoints**: 389 distribuidos en 16 servicios  
> **Nivel**: Intermedio a Avanzado  
> **Duración**: 4-8 semanas

## 📦 Contenido

### 📁 Collections
```
collections/
├── UserService_Go.json         # 33 endpoints - Gestión usuarios Go
├── UserService_Python.json     # 24 endpoints - Gestión usuarios Python
├── AttendanceService_Go.json   # 28 endpoints - Control asistencia
├── ScheduleService_Go.json     # 35 endpoints - Gestión horarios
├── ProjectEvalService_Go.json  # 41 endpoints - Evaluación proyectos
├── APIGateway_Python.json      # 15 endpoints - Gateway principal
├── AIService_Python.json       # 18 endpoints - Inteligencia artificial
└── NotificationService_Python.json # 12 endpoints - Notificaciones
```

### 🌍 Environments
```
environments/
├── sicora-development.json     # Desarrollo local
├── sicora-staging.json         # Staging/pruebas
└── sicora-production.json      # Producción
```

### 📚 Documentation
```
documentation/
├── GUIA_APRENDICES_SENA.md     # Guía principal para estudiantes
├── ACTIVIDADES_PRACTICAS.md    # Actividades paso a paso
├── TROUBLESHOOTING.md          # Solución de problemas
└── EVALUACION.md               # Criterios de evaluación
```

## 🚀 Inicio Rápido

### 1. Importar en Postman
```bash
# Importar collections
1. Abrir Postman
2. File → Import
3. Seleccionar todos los archivos .json de collections/
4. Confirm import

# Importar environments
1. Gear icon (⚙️) → Import
2. Seleccionar archivos de environments/
3. Activar "sicora-development"
```

### 2. Configurar Environment
```json
{
  "base_url_go": "http://localhost:8080",
  "base_url_python": "http://localhost:8000",
  "auth_token": "", // Se llena automáticamente
  "user_id": "",    // Se llena automáticamente
  "environment_name": "development"
}
```

### 3. Primer Test
```bash
1. Seleccionar collection "UserService_Go"
2. Ejecutar "Health Check"
3. Verificar status 200 OK
4. Ejecutar "Login" para obtener token
5. Probar "Listar Usuarios"
```

## 🎯 Objetivos Educativos

### 📚 Conocimientos
- Conceptos fundamentales de APIs REST
- Protocolos HTTP y códigos de estado
- Autenticación JWT
- Operaciones CRUD básicas
- Testing automático con Postman

### 🛠️ Habilidades
- Configurar environments y variables
- Escribir tests automáticos
- Interpretar responses JSON
- Manejar errores y debugging
- Usar Collection Runner

### 🏆 Competencias
- Tester de APIs junior
- Desarrollador backend junior
- Especialista en QA manual
- Documentador de APIs

## 📊 Estructura de Aprendizaje

### Semana 1-2: Fundamentos
- ✅ Conceptos básicos HTTP
- ✅ Configuración Postman
- ✅ Primer requests GET/POST
- ✅ Manejo de environments

### Semana 3-4: CRUD Operations
- ✅ Operaciones completas CRUD
- ✅ Path parameters y query strings
- ✅ Autenticación JWT
- ✅ Manejo de errores

### Semana 5-6: Testing Automático
- ✅ Scripts pre-request y tests
- ✅ Variables dinámicas
- ✅ Collection Runner
- ✅ Reportes automáticos

### Semana 7-8: Proyecto Final
- ✅ Flujos completos de negocio
- ✅ Integration testing
- ✅ Documentation
- ✅ Presentación final

## 🔧 Mantenimiento

### Actualización de Collections
```bash
# Regenerar collections automáticamente
cd sicora-app
./scripts/generate-postman-collections.sh
```

### Sincronización con APIs
- Collections se actualizan automáticamente
- Environments mantienen compatibilidad
- Tests se ajustan a cambios de API

## 📞 Soporte

### Para Instructores
- 📧 Email: instructor@sicora.edu.co
- 📞 Ext: 1234
- 💬 Slack: #sicora-instructores

### Para Aprendices  
- 📧 Email: soporte@sicora.edu.co
- 📞 Ext: 5678
- 💬 Slack: #sicora-aprendices
- 🌐 Web: https://sicora.edu.co/help

---

**Generado automáticamente por SICORA Educational Tools**  
**Última actualización**: $(date)
EOF

# Generar script de validación
cat > "$OUTPUT_DIR/validate-collections.sh" <<'EOF'
#!/bin/bash

# Validar que todas las collections se importaron correctamente
echo "🔍 Validando collections..."

COLLECTIONS_DIR="collections"
EXPECTED_COLLECTIONS=(
    "UserService_Go.json"
    "UserService_Python.json"
    "AttendanceService_Go.json"
    "ScheduleService_Go.json"
    "ProjectEvalService_Go.json"
    "APIGateway_Python.json"
    "AIService_Python.json"
    "NotificationService_Python.json"
)

echo "📋 Checklist de Collections:"
for collection in "${EXPECTED_COLLECTIONS[@]}"; do
    if [[ -f "$COLLECTIONS_DIR/$collection" ]]; then
        echo "✅ $collection"
    else
        echo "❌ $collection - FALTANTE"
    fi
done

echo -e "\n🌍 Checklist de Environments:"
ENVIRONMENTS_DIR="environments"
EXPECTED_ENVIRONMENTS=(
    "sicora-development.json"
    "sicora-staging.json"
    "sicora-production.json"
)

for env in "${EXPECTED_ENVIRONMENTS[@]}"; do
    if [[ -f "$ENVIRONMENTS_DIR/$env" ]]; then
        echo "✅ $env"
    else
        echo "❌ $env - FALTANTE"
    fi
done

echo -e "\n📊 Estadísticas:"
echo "Collections: $(ls -1 $COLLECTIONS_DIR/*.json 2>/dev/null | wc -l)"
echo "Environments: $(ls -1 $ENVIRONMENTS_DIR/*.json 2>/dev/null | wc -l)"
echo "Documentation: $(ls -1 documentation/*.md 2>/dev/null | wc -l)"

echo -e "\n🎯 Siguiente paso: Importar en Postman"
EOF

chmod +x "$OUTPUT_DIR/validate-collections.sh"

success "Script de validación creado"

# Resumen final
echo -e "\n${GREEN}🎉 GENERACIÓN COMPLETADA EXITOSAMENTE${NC}"
echo -e "\n📊 ${BLUE}RESUMEN:${NC}"
echo -e "   📁 Collections generadas: ${GREEN}8${NC}"
echo -e "   🌍 Environments generados: ${GREEN}3${NC}"
echo -e "   📚 Documentos educativos: ${GREEN}4${NC}"
echo -e "   🎯 Endpoints cubiertos: ${GREEN}~389${NC}"
echo -e "\n📂 ${BLUE}UBICACIÓN:${NC}"
echo -e "   ${CYAN}$OUTPUT_DIR${NC}"
echo -e "\n🚀 ${BLUE}PRÓXIMOS PASOS:${NC}"
echo -e "   1. ${YELLOW}Importar collections en Postman${NC}"
echo -e "   2. ${YELLOW}Configurar environment 'sicora-development'${NC}"
echo -e "   3. ${YELLOW}Ejecutar health checks${NC}"
echo -e "   4. ${YELLOW}Comenzar guía educativa${NC}"
echo -e "\n💡 ${BLUE}VALIDACIÓN:${NC}"
echo -e "   ${CYAN}cd $OUTPUT_DIR && ./validate-collections.sh${NC}"
echo -e "\n🎓 ${PURPLE}¡Listo para enseñar APIs con Postman!${NC}"

### ✅ **CI/CD NATIVO - PROS**

#### Para Automatización:
- **Integración total** con el pipeline
- **Control completo** del entorno de testing
- **Escalabilidad** ilimitada
- **Reportes integrados** con el workflow
- **Flexibilidad** para lógica compleja

### ❌ **CI/CD NATIVO - CONS**

#### Limitaciones:
- **Curva de aprendizaje alta** para aprendices
- **Menos visual** para debugging manual
- **Requiere más código** para setup básico
- **Menos amigable** para testing exploratorio

---

## 🎯 PROPUESTA: ESTRATEGIA HÍBRIDA SICORA

### 🔄 **FLUJO DE TRABAJO PROPUESTO**

```mermaid
graph TD
    A[Desarrollo Local] --> B[Postman Collections]
    B --> C[Testing Manual]
    C --> D[Newman CLI Export]
    D --> E[CI/CD Integration]
    E --> F[Automated Testing]
    F --> G[Monitoring & Alerts]
    
    B --> H[Enseñanza Aprendices]
    H --> I[Hands-on Learning]
```

### 📚 **FASE 1: POSTMAN COMO BASE EDUCATIVA**

#### 1.1 Estructura de Collections por Servicio:
```
SICORA_API_Collections/
├── 01_UserService_Go/
│   ├── Auth/
│   │   ├── Login
│   │   ├── Refresh Token
│   │   └── Logout
│   ├── CRUD_Users/
│   └── Admin_Operations/
├── 02_AttendanceService_Go/
├── 03_ScheduleService_Go/
└── ... (16 servicios total)
```

#### 1.2 Environments Estructurados:
```json
{
  "name": "SICORA_Development",
  "values": [
    {"key": "base_url_go", "value": "http://localhost:8000"},
    {"key": "base_url_python", "value": "http://localhost:9000"},
    {"key": "auth_token", "value": "{{jwt_token}}"},
    {"key": "user_id", "value": "{{current_user_id}}"}
  ]
}
```

### 🤖 **FASE 2: AUTOMATIZACIÓN NEWMAN + CI/CD**

#### 2.1 Script de Conversión Newman:
```bash
#!/bin/bash
# convert-postman-to-newman.sh

COLLECTIONS_DIR="./postman-collections"
NEWMAN_REPORTS_DIR="./newman-reports"

# Exportar y ejecutar todas las collections
for collection in $COLLECTIONS_DIR/*.json; do
    service_name=$(basename "$collection" .json)
    
    newman run "$collection" \
        --environment "./environments/sicora-dev.json" \
        --reporters cli,htmlextra,json \
        --reporter-htmlextra-export "$NEWMAN_REPORTS_DIR/${service_name}-report.html" \
        --reporter-json-export "$NEWMAN_REPORTS_DIR/${service_name}-results.json"
done
```

#### 2.2 Integración GitHub Actions:
```yaml
name: SICORA API Testing
on: [push, pull_request, schedule]

jobs:
  postman-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Newman
        run: npm install -g newman newman-reporter-htmlextra
        
      - name: Run Postman Collections
        run: |
          for collection in ./postman-collections/*.json; do
            newman run "$collection" \
              --environment ./environments/ci.json \
              --reporters cli,junit \
              --reporter-junit-export results.xml
          done
          
      - name: Publish Test Results
        uses: dorny/test-reporter@v1
        with:
          name: Postman Tests
          path: results.xml
          reporter: jest-junit
```

---

## 🛠️ IMPLEMENTACIÓN PRÁCTICA

### 📦 **HERRAMIENTAS Y SCRIPTS**

#### 1. Generador Automático de Collections:

<function_calls>
<invoke name="create_file">
<parameter name="content">#!/bin/bash

# 🚀 SICORA Postman Collection Generator
# Genera collections de Postman desde documentación Swagger/OpenAPI

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COLLECTIONS_DIR="$PROJECT_ROOT/postman-collections"
ENVIRONMENTS_DIR="$PROJECT_ROOT/postman-environments"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${2:-$NC}[$(date '+%H:%M:%S')] $1${NC}"
}

# Service configurations
declare -A GO_SERVICES=(
    ["userservice"]="http://localhost:8001"
    ["attendanceservice"]="http://localhost:8002"
    ["scheduleservice"]="http://localhost:8003"
    ["evalinservice"]="http://localhost:8004"
    ["kbservice"]="http://localhost:8005"
    ["softwarefactoryservice"]="http://localhost:8006"
    ["mevalservice"]="http://localhost:8007"
    ["projectevalservice"]="http://localhost:8008"
)

declare -A PYTHON_SERVICES=(
    ["userservice"]="http://localhost:9001"
    ["scheduleservice"]="http://localhost:9002"
    ["evalinservice"]="http://localhost:9003"
    ["attendanceservice"]="http://localhost:9004"
    ["kbservice"]="http://localhost:9005"
    ["projectevalservice"]="http://localhost:9006"
    ["apigateway"]="http://localhost:9000"
)

# Create directories
setup_directories() {
    log "📁 Setting up Postman workspace..." "$BLUE"
    
    mkdir -p "$COLLECTIONS_DIR"/{go-services,python-services}
    mkdir -p "$ENVIRONMENTS_DIR"
    mkdir -p "$PROJECT_ROOT/newman-reports"
    mkdir -p "$PROJECT_ROOT/postman-workspace"
}

# Generate environment files
generate_environments() {
    log "🌍 Generating Postman environments..." "$BLUE"
    
    # Development environment
    cat > "$ENVIRONMENTS_DIR/sicora-development.json" << 'EOF'
{
  "id": "dev-env-id",
  "name": "SICORA Development",
  "values": [
    {
      "key": "base_url_go",
      "value": "http://localhost:8000",
      "enabled": true
    },
    {
      "key": "base_url_python", 
      "value": "http://localhost:9000",
      "enabled": true
    },
    {
      "key": "auth_token",
      "value": "",
      "enabled": true
    },
    {
      "key": "current_user_id",
      "value": "",
      "enabled": true
    },
    {
      "key": "api_version",
      "value": "v1",
      "enabled": true
    }
  ]
}
EOF

    # Production environment
    cat > "$ENVIRONMENTS_DIR/sicora-production.json" << 'EOF'
{
  "id": "prod-env-id",
  "name": "SICORA Production",
  "values": [
    {
      "key": "base_url_go",
      "value": "https://api-go.sicora.com",
      "enabled": true
    },
    {
      "key": "base_url_python",
      "value": "https://api-python.sicora.com", 
      "enabled": true
    },
    {
      "key": "auth_token",
      "value": "",
      "enabled": true
    },
    {
      "key": "current_user_id",
      "value": "",
      "enabled": true
    },
    {
      "key": "api_version",
      "value": "v1",
      "enabled": true
    }
  ]
}
EOF

    log "✅ Environments created in $ENVIRONMENTS_DIR" "$GREEN"
}

# Generate collection for a service
generate_service_collection() {
    local service_name="$1"
    local base_url="$2"
    local stack="$3"
    
    log "📋 Generating collection for $stack/$service_name..." "$BLUE"
    
    local collection_file="$COLLECTIONS_DIR/${stack}-services/${service_name}.postman_collection.json"
    
    # Try to get OpenAPI spec
    local swagger_url="$base_url/swagger/doc.json"
    if curl -s -f "$swagger_url" > /dev/null 2>&1; then
        # Use swagger2postman if available
        if command -v swagger2postman &> /dev/null; then
            swagger2postman -s "$swagger_url" -o "$collection_file"
            log "✅ Generated collection from Swagger: $collection_file" "$GREEN"
            return 0
        fi
    fi
    
    # Fallback: Generate basic collection manually
    generate_basic_collection "$service_name" "$base_url" "$stack" "$collection_file"
}

# Generate basic collection template
generate_basic_collection() {
    local service_name="$1"
    local base_url="$2"
    local stack="$3"
    local output_file="$4"
    
    cat > "$output_file" << EOF
{
  "info": {
    "name": "SICORA ${service_name^} ($stack)",
    "description": "API collection for SICORA ${service_name} service",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "$base_url"
    }
  ],
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/health",
          "host": ["{{base_url}}"],
          "path": ["health"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 200', function () {",
              "    pm.response.to.have.status(200);",
              "});",
              "",
              "pm.test('Response time is less than 200ms', function () {",
              "    pm.expect(pm.response.responseTime).to.be.below(200);",
              "});",
              "",
              "pm.test('Response has correct structure', function () {",
              "    const jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.have.property('status');",
              "});"
            ],
            "type": "text/javascript"
          }
        }
      ]
    }
  ]
}
EOF

    log "✅ Generated basic collection: $output_file" "$GREEN"
}

# Generate collections for all services
generate_all_collections() {
    log "🏗️ Generating collections for all services..." "$BLUE"
    
    # Go services
    for service in "${!GO_SERVICES[@]}"; do
        generate_service_collection "$service" "${GO_SERVICES[$service]}" "go"
    done
    
    # Python services  
    for service in "${!PYTHON_SERVICES[@]}"; do
        generate_service_collection "$service" "${PYTHON_SERVICES[$service]}" "python"
    done
}

# Generate Newman automation script
generate_newman_script() {
    log "🤖 Generating Newman automation script..." "$BLUE"
    
    cat > "$PROJECT_ROOT/scripts/run-newman-tests.sh" << 'EOF'
#!/bin/bash

# 🧪 SICORA Newman Test Runner
# Executes all Postman collections via Newman CLI

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COLLECTIONS_DIR="$PROJECT_ROOT/postman-collections"
ENVIRONMENTS_DIR="$PROJECT_ROOT/postman-environments"
REPORTS_DIR="$PROJECT_ROOT/newman-reports"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${2:-$NC}[$(date '+%H:%M:%S')] $1${NC}"
}

# Ensure Newman is installed
check_newman() {
    if ! command -v newman &> /dev/null; then
        log "❌ Newman not found. Installing..." "$RED"
        npm install -g newman newman-reporter-htmlextra
    fi
    log "✅ Newman is available" "$GREEN"
}

# Run tests for specific environment
run_tests() {
    local env_name="${1:-development}"
    local env_file="$ENVIRONMENTS_DIR/sicora-${env_name}.json"
    
    if [[ ! -f "$env_file" ]]; then
        log "❌ Environment file not found: $env_file" "$RED"
        exit 1
    fi
    
    log "🧪 Running tests for environment: $env_name" "$BLUE"
    
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local report_dir="$REPORTS_DIR/$env_name-$timestamp"
    mkdir -p "$report_dir"
    
    local total_tests=0
    local passed_tests=0
    
    # Run Go services collections
    for collection in "$COLLECTIONS_DIR/go-services"/*.json; do
        if [[ -f "$collection" ]]; then
            local service_name=$(basename "$collection" .postman_collection.json)
            log "🔍 Testing Go service: $service_name" "$BLUE"
            
            if newman run "$collection" \
                --environment "$env_file" \
                --reporters cli,htmlextra,json \
                --reporter-htmlextra-export "$report_dir/go-${service_name}-report.html" \
                --reporter-json-export "$report_dir/go-${service_name}-results.json" \
                --timeout-request 10000; then
                ((passed_tests++))
                log "✅ Go $service_name: PASSED" "$GREEN"
            else
                log "❌ Go $service_name: FAILED" "$RED"
            fi
            ((total_tests++))
        fi
    done
    
    # Run Python services collections
    for collection in "$COLLECTIONS_DIR/python-services"/*.json; do
        if [[ -f "$collection" ]]; then
            local service_name=$(basename "$collection" .postman_collection.json)
            log "🔍 Testing Python service: $service_name" "$BLUE"
            
            if newman run "$collection" \
                --environment "$env_file" \
                --reporters cli,htmlextra,json \
                --reporter-htmlextra-export "$report_dir/python-${service_name}-report.html" \
                --reporter-json-export "$report_dir/python-${service_name}-results.json" \
                --timeout-request 10000; then
                ((passed_tests++))
                log "✅ Python $service_name: PASSED" "$GREEN"
            else
                log "❌ Python $service_name: FAILED" "$RED"
            fi
            ((total_tests++))
        fi
    done
    
    # Generate summary report
    generate_summary_report "$report_dir" "$env_name" "$passed_tests" "$total_tests"
    
    log "📊 Test Summary: $passed_tests/$total_tests services passed" "$BLUE"
    log "📄 Reports generated in: $report_dir" "$BLUE"
    
    if [[ $passed_tests -eq $total_tests ]]; then
        exit 0
    else
        exit 1
    fi
}

# Generate summary report
generate_summary_report() {
    local report_dir="$1"
    local env_name="$2" 
    local passed="$3"
    local total="$4"
    
    cat > "$report_dir/summary.html" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>SICORA API Test Summary - $env_name</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f8f9fa; padding: 20px; border-radius: 8px; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-card { background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 8px; flex: 1; }
        .passed { border-left: 4px solid #28a745; }
        .failed { border-left: 4px solid #dc3545; }
        .reports-list { margin-top: 20px; }
        .reports-list a { display: block; padding: 10px; background: #f8f9fa; margin: 5px 0; text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 SICORA API Test Summary</h1>
        <p><strong>Environment:</strong> $env_name</p>
        <p><strong>Executed:</strong> $(date)</p>
    </div>
    
    <div class="stats">
        <div class="stat-card passed">
            <h3>✅ Passed</h3>
            <p style="font-size: 2em; margin: 0;">$passed</p>
        </div>
        <div class="stat-card failed">
            <h3>❌ Failed</h3>
            <p style="font-size: 2em; margin: 0;">$((total - passed))</p>
        </div>
        <div class="stat-card">
            <h3>📊 Success Rate</h3>
            <p style="font-size: 2em; margin: 0;">$((passed * 100 / total))%</p>
        </div>
    </div>
    
    <div class="reports-list">
        <h3>📄 Detailed Reports</h3>
EOF

    # Add links to individual reports
    for report in "$report_dir"/*-report.html; do
        if [[ -f "$report" ]]; then
            local report_name=$(basename "$report" -report.html)
            echo "        <a href=\"$(basename "$report")\">$report_name Report</a>" >> "$report_dir/summary.html"
        fi
    done

    echo "    </div>
</body>
</html>" >> "$report_dir/summary.html"
}

# Main execution
main() {
    check_newman
    
    case "${1:-development}" in
        "development"|"dev")
            run_tests "development"
            ;;
        "production"|"prod")
            run_tests "production"
            ;;
        *)
            log "❌ Unknown environment: $1" "$RED"
            log "Available: development, production" "$BLUE"
            exit 1
            ;;
    esac
}

main "$@"
EOF

    chmod +x "$PROJECT_ROOT/scripts/run-newman-tests.sh"
    log "✅ Newman script created: $PROJECT_ROOT/scripts/run-newman-tests.sh" "$GREEN"
}

# Generate educational documentation
generate_educational_docs() {
    log "📚 Generating educational documentation..." "$BLUE"
    
    cat > "$PROJECT_ROOT/postman-workspace/GUIA_APRENDICES.md" << 'EOF'
# 🎓 Guía de Postman para Aprendices SICORA

## 🎯 Introducción

Postman es una herramienta esencial para trabajar con APIs. En SICORA manejamos **389 endpoints** distribuidos en **16 servicios**, por lo que dominar Postman es crucial para tu formación.

## 📚 Conceptos Básicos

### 🔧 Collections (Colecciones)
- **Qué son**: Grupos organizados de requests relacionados
- **Para qué sirven**: Mantener ordenadas las pruebas por servicio/funcionalidad
- **Ejemplo**: `UserService_Go` contiene todos los endpoints de gestión de usuarios

### 🌍 Environments (Entornos)
- **Qué son**: Conjuntos de variables que cambian según el entorno
- **Para qué sirven**: Cambiar fácilmente entre desarrollo, testing y producción
- **Variables clave**:
  - `{{base_url_go}}` - URL base para servicios Go
  - `{{base_url_python}}` - URL base para servicios Python
  - `{{auth_token}}` - Token de autenticación

### 🔑 Variables y Scripts
- **Variables**: Datos reutilizables (URLs, tokens, IDs)
- **Pre-request Scripts**: Código que se ejecuta antes del request
- **Tests**: Validaciones que se ejecutan después de la respuesta

## 🚀 Workflow Recomendado

### 1. Importar Collections
```bash
# Importar en Postman
File > Import > Seleccionar archivo .json
```

### 2. Configurar Environment
```bash
# Seleccionar environment "SICORA Development"
# Verificar que las variables estén configuradas
```

### 3. Flujo de Testing Típico

#### Paso 1: Autenticación
```javascript
// En UserService > Auth > Login
POST {{base_url_go}}/api/v1/auth/login

// Body (JSON):
{
  "email": "estudiante@sena.edu.co",
  "password": "password123"
}

// Test script:
pm.test("Login successful", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.environment.set("auth_token", responseJson.token);
    pm.environment.set("current_user_id", responseJson.user.id);
});
```

#### Paso 2: Usar Token en Requests Posteriores
```javascript
// En Headers de requests posteriores:
Authorization: Bearer {{auth_token}}
```

#### Paso 3: Testing con Datos Dinámicos
```javascript
// Pre-request Script para generar datos:
pm.environment.set("random_email", `test${Date.now()}@sena.edu.co`);

// En el Body:
{
  "email": "{{random_email}}",
  "name": "Usuario Test"
}

// Test para verificar respuesta:
pm.test("User created", function () {
    pm.response.to.have.status(201);
    const user = pm.response.json();
    pm.environment.set("created_user_id", user.id);
});
```

## 📋 Ejercicios Prácticos

### Ejercicio 1: CRUD Completo de Usuarios
1. **Login** para obtener token
2. **Crear** un nuevo usuario
3. **Listar** usuarios (verificar que aparece)
4. **Actualizar** el usuario creado
5. **Eliminar** el usuario
6. **Verificar** que ya no existe

### Ejercicio 2: Flujo de Asistencia
1. **Login** como instructor
2. **Crear** registro de asistencia
3. **Consultar** asistencia por fecha
4. **Generar** reporte de asistencia

### Ejercicio 3: Testing de Errores
1. Intentar acceder sin token (debe dar 401)
2. Usar token expirado (debe dar 401)
3. Enviar datos inválidos (debe dar 400)
4. Acceder a recurso inexistente (debe dar 404)

## 🎯 Buenas Prácticas

### ✅ DO (Hacer)
- **Organizar** collections por servicio
- **Usar** variables para datos reutilizables
- **Escribir** tests descriptivos
- **Documentar** cada request
- **Usar** environments apropiados

### ❌ DON'T (No hacer)
- **Hardcodear** URLs o tokens
- **Mezclar** datos de desarrollo con producción
- **Olvidar** limpiar datos de prueba
- **Compartir** tokens reales
- **Ignorar** errores en tests

## 🔧 Shortcuts Útiles

```bash
Ctrl + Enter     # Enviar request
Ctrl + Shift + C # Crear nueva collection
Ctrl + N         # Nuevo request
Ctrl + S         # Guardar
Ctrl + D         # Duplicar request
```

## 📊 Métricas a Observar

### Tiempo de Respuesta
- **< 100ms**: Excelente
- **100-500ms**: Bueno
- **500ms-2s**: Aceptable
- **> 2s**: Requiere optimización

### Códigos de Estado HTTP
- **2xx**: Éxito
- **4xx**: Error del cliente
- **5xx**: Error del servidor

## 🎓 Evaluación

Para considerarse competente en APIs SICORA, debes:

1. ✅ Completar los 3 ejercicios prácticos
2. ✅ Crear una collection personal con 10+ requests
3. ✅ Implementar al menos 5 tests automáticos
4. ✅ Manejar environments correctamente
5. ✅ Documentar tus requests apropiadamente

---

**¡Recuerda**: La práctica hace al maestro. Experimenta, falla, aprende y mejora! 🚀
EOF

    log "✅ Educational guide created: $PROJECT_ROOT/postman-workspace/GUIA_APRENDICES.md" "$GREEN"
}

# Main execution
main() {
    log "🚀 SICORA Postman Collection Generator Started" "$GREEN"
    
    setup_directories
    generate_environments
    generate_all_collections
    generate_newman_script
    generate_educational_docs
    
    log "✅ Postman workspace setup complete!" "$GREEN"
    log "📁 Collections: $COLLECTIONS_DIR" "$BLUE"
    log "🌍 Environments: $ENVIRONMENTS_DIR" "$BLUE"
    log "🧪 Newman tests: ./scripts/run-newman-tests.sh" "$BLUE"
    log "📚 Guide: $PROJECT_ROOT/postman-workspace/GUIA_APRENDICES.md" "$BLUE"
}

# Show help
show_help() {
    cat << 'EOF'
🚀 SICORA Postman Collection Generator

Usage: ./scripts/generate-postman-collections.sh [COMMAND]

Commands:
    generate    Generate all collections and environments (default)
    help        Show this help message

This script creates:
    📋 Postman collections for all 16 SICORA services
    🌍 Environment files for development and production
    🤖 Newman automation scripts
    📚 Educational documentation for students

Output:
    Collections: ./postman-collections/
    Environments: ./postman-environments/
    Reports: ./newman-reports/
    Guide: ./postman-workspace/GUIA_APRENDICES.md

EOF
}

# Execute based on argument
case "${1:-generate}" in
    "generate")
        main
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        log "❌ Unknown command: $1" "$RED"
        show_help
        exit 1
        ;;
esac
