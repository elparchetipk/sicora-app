# 🎓 SICORA Postman Collections - Educativo

> Collections educativas para estudiantes OneVision Open Source
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
├── GUIA_ESTUDIANTES_ONEVISION.md  # Guía principal para estudiantes
├── ACTIVIDADES_PRACTICAS.md       # Actividades paso a paso
├── TROUBLESHOOTING.md             # Solución de problemas
└── EVALUACION.md                  # Criterios de evaluación
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
  "user_id": "", // Se llena automáticamente
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
