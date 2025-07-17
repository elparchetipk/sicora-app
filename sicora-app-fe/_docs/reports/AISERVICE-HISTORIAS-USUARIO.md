# 🤖 AIService - Historias de Usuario

**Fecha:** 17 de junio de 2025  
**Estado:** 0% implementado - Solo estructura básica con endpoints mock  
**Prioridad:** CRÍTICA - Completar FastAPI al 100% antes de otros stacks

---

## 📋 **HISTORIAS DE USUARIO - AISERVICE**

### **🤖 Chat y Reglamento Académico**

**HU-AI-001: Iniciar Conversación con Chatbot**

- **Como** Frontend/Usuario
- **Quiero** poder iniciar una conversación con `POST /api/v1/ai/chat/conversations`
- **Para** crear una nueva sesión de chatbot de reglamento académico
- **Estado**: 📋 **PENDIENTE** - Implementar creación de conversación con IA

**HU-AI-002: Enviar Mensaje al Chatbot**

- **Como** Frontend/Usuario
- **Quiero** poder enviar mensajes con `POST /api/v1/ai/chat/conversations/{id}/messages`
- **Para** recibir respuestas inteligentes sobre reglamento SENA
- **Estado**: 📋 **PENDIENTE** - Implementar procesamiento IA + integración OpenAI

**HU-AI-003: Obtener Historial de Conversación**

- **Como** Frontend/Usuario
- **Quiero** poder consultar el historial con `GET /api/v1/ai/chat/conversations/{id}`
- **Para** revisar mensajes anteriores de la conversación
- **Estado**: 📋 **PENDIENTE** - Implementar almacenamiento y recuperación

### **📊 Análisis Predictivo**

**HU-AI-004: Análisis Predictivo de Asistencia**

- **Como** Administrador/Instructor
- **Quiero** poder solicitar análisis con `POST /api/v1/ai/analytics/attendance-prediction`
- **Para** identificar patrones de riesgo de deserción
- **Estado**: 📋 **PENDIENTE** - Implementar ML básico para predicciones

**HU-AI-005: Generar Alertas Automáticas**

- **Como** Sistema
- **Quiero** poder generar alertas automáticas con `POST /api/v1/ai/alerts/generate`
- **Para** notificar automáticamente situaciones de riesgo académico
- **Estado**: 📋 **PENDIENTE** - Implementar sistema de alertas inteligentes

### **🎯 Gestión de Modelos IA**

**HU-AI-006: Listar Modelos de IA Disponibles**

- **Como** Administrador
- **Quiero** poder consultar modelos con `GET /api/v1/ai/models`
- **Para** verificar qué modelos de IA están configurados y disponibles
- **Estado**: 📋 **PENDIENTE** - Implementar gestión de modelos (OpenAI, local, etc.)

**HU-AI-007: Probar Modelo de IA**

- **Como** Administrador
- **Quiero** poder probar modelos con `POST /api/v1/ai/models/{model_id}/test`
- **Para** verificar que los modelos funcionan correctamente
- **Estado**: 📋 **PENDIENTE** - Implementar testing de modelos

### **📚 Gestión de Conocimiento para IA**

**HU-AI-008: Gestionar Base de Conocimiento IA**

- **Como** Administrador
- **Quiero** poder gestionar contenido con `POST /api/v1/ai/knowledge`
- **Para** mantener actualizada la base de conocimiento del chatbot
- **Estado**: 📋 **PENDIENTE** - Implementar integración con KbService

---

## 🏗️ **ARQUITECTURA A IMPLEMENTAR**

### **Domain Layer**

```python
# Entidades
- Conversation (id, user_id, created_at, updated_at, status)
- Message (id, conversation_id, content, role, timestamp)
- AIModel (id, name, provider, status, config)
- PredictionResult (id, type, confidence, data, created_at)

# Value Objects
- MessageRole (user, assistant, system)
- ModelProvider (openai, huggingface, local)
- PredictionType (attendance, dropout, performance)
```

### **Application Layer**

```python
# Use Cases
- CreateConversationUseCase
- SendMessageUseCase
- GetConversationHistoryUseCase
- PredictAttendanceUseCase
- GenerateAlertsUseCase
- ManageModelsUseCase
- UpdateKnowledgeBaseUseCase
- TestModelUseCase
```

### **Infrastructure Layer**

```python
# Servicios externos
- OpenAIService (integración con API)
- EmbeddingService (para búsqueda semántica)
- ModelManagerService (gestión de modelos)
- KnowledgeBaseIntegration (conexión con KbService)
```

---

## 🚀 **PLAN DE IMPLEMENTACIÓN**

### **Día 1: Entidades y Casos de Uso Básicos**

1. Implementar domain entities y value objects
2. Crear use cases para conversaciones básicas
3. Setup base de datos con migraciones

### **Día 2: Integración OpenAI**

1. Configurar OpenAI service
2. Implementar chatbot básico funcional
3. Testing de integración IA

### **Día 3: Análisis Predictivo Básico**

1. Implementar predicciones simples
2. Sistema de alertas automáticas
3. Integración con AttendanceService

### **Día 4: Gestión de Modelos**

1. CRUD de modelos IA
2. Testing y validación de modelos
3. Configuración dinámica

### **Día 5: Testing e Integración**

1. Tests unitarios completos
2. Tests de integración
3. Documentación final

---

## 🎯 **CRITERIOS DE ÉXITO**

### **Definición de "Completado":**

- ✅ **8/8 Historias de Usuario** implementadas
- ✅ **Chatbot funcional** con OpenAI integration
- ✅ **Análisis predictivo básico** operativo
- ✅ **Tests > 80%** coverage
- ✅ **Clean Architecture** validada
- ✅ **Swagger** documentación completa

### **Entregables:**

- AIService completamente funcional
- FastAPI stack al 100% para usar como referencia
- Base sólida para implementar en otros stacks

---

**¿Comenzamos con la implementación del AIService para completar FastAPI al 100%?**
