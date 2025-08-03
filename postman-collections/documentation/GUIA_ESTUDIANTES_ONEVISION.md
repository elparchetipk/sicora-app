# 🎓 Guía para Estudiantes OneVision - SICORA API Testing

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
