# 🧪 **INSTRUCCIONES DE TESTING - SERVICIOS CORE**

**Fecha:** 14 de junio de 2025  
**Servicios actualizados:** OpenAIEmbeddingService, HybridSearchService

---

## 📋 **PREREQUISITOS**

1. Asegurate de estar en el directorio del proyecto:
```bash
cd /home/epti/Documentos/epti-dev/asiste-app/fast-rn/sicora-app-be-multistack/01-fastapi/kbservice
```

2. Activar el entorno virtual:
```bash
source ../venv/bin/activate
```

3. Instalar dependencias actualizadas:
```bash
pip install -r requirements.txt
```

---

## 🔬 **TESTS UNITARIOS**

### **1. Test OpenAI Embedding Service**
```bash
# Ejecutar tests específicos del embedding service
pytest tests/unit/test_openai_embedding_service.py -v

# Ejecutar con cobertura
pytest tests/unit/test_openai_embedding_service.py --cov=app.infrastructure.services.kb_services_impl --cov-report=term-missing
```

**Casos de test incluidos:**
- ✅ Generación de embeddings en modo mock
- ✅ Embeddings determinísticos 
- ✅ Manejo de texto vacío
- ✅ Procesamiento por lotes
- ✅ Integración con API de OpenAI (mocked)
- ✅ Manejo de errores de API
- ✅ Validación de dimensiones
- ✅ Truncamiento de texto largo

### **2. Test Hybrid Search Service**
```bash
# Ejecutar tests específicos del search service
pytest tests/unit/test_hybrid_search_service.py -v

# Ejecutar con cobertura
pytest tests/unit/test_hybrid_search_service.py --cov=app.infrastructure.services.kb_services_impl --cov-report=term-missing
```

**Casos de test incluidos:**
- ✅ Búsqueda híbrida exitosa
- ✅ Filtros por rol de usuario
- ✅ Búsqueda semántica
- ✅ Búsqueda de texto
- ✅ Items relacionados
- ✅ Manejo de errores
- ✅ Combinación de resultados

### **3. Ejecutar todos los tests unitarios**
```bash
# Todos los tests unitarios
pytest tests/unit/ -v

# Con reporte de cobertura completo
pytest tests/unit/ --cov=app --cov-report=html --cov-report=term-missing
```

---

## 🔧 **TESTS DE INTEGRACIÓN**

### **1. Test de importación de servicios**
```bash
# Verificar que los servicios se pueden importar sin errores
python -c "
from app.infrastructure.services.kb_services_impl import OpenAIEmbeddingService, HybridSearchService
print('✅ Importación exitosa de servicios')
"
```

### **2. Test de configuración**
```bash
# Verificar configuraciones
python -c "
from app.config import settings
print(f'Embedding model: {settings.EMBEDDING_MODEL}')
print(f'Embedding dimension: {settings.EMBEDDING_DIMENSION}')
print(f'OpenAI batch size: {settings.OPENAI_BATCH_SIZE}')
print(f'Request timeout: {settings.OPENAI_REQUEST_TIMEOUT}')
print('✅ Configuraciones cargadas correctamente')
"
```

### **3. Test de servicio con datos mock**
```bash
# Test básico del embedding service en modo mock
python -c "
import asyncio
from app.infrastructure.services.kb_services_impl import OpenAIEmbeddingService

async def test_mock_embedding():
    service = OpenAIEmbeddingService()
    result = await service.generate_embedding('Texto de prueba')
    print(f'✅ Embedding generado: {len(result.values)} dimensiones')
    
    # Test batch
    batch_result = await service.generate_embeddings_batch(['Texto 1', 'Texto 2'])
    print(f'✅ Batch embeddings: {len(batch_result)} vectores')

asyncio.run(test_mock_embedding())
"
```

---

## 🚀 **TESTS OPCIONALES CON API REAL**

**⚠️ Nota:** Estos tests requieren una API key válida de OpenAI.

### **1. Configurar API Key (opcional)**
```bash
# Exportar API key temporalmente para testing
export OPENAI_API_KEY="tu-api-key-aqui"
```

### **2. Test con API real**
```bash
# Test con API real (solo si tienes API key)
python -c "
import asyncio
import os
from app.infrastructure.services.kb_services_impl import OpenAIEmbeddingService

async def test_real_api():
    if os.getenv('OPENAI_API_KEY'):
        service = OpenAIEmbeddingService()
        result = await service.generate_embedding('Sistema de asistencia académica')
        print(f'✅ API real: embedding de {len(result.values)} dimensiones')
        print(f'Primera dimensión: {result.values[0]:.6f}')
    else:
        print('⚠️ No API key configurada, usando modo mock')

asyncio.run(test_real_api())
"
```

---

## 📊 **VERIFICACIÓN DE RESULTADOS**

### **Resultados esperados:**

1. **OpenAI Embedding Service:**
   - ✅ 12/12 tests pasando
   - ✅ Embeddings de 1536 dimensiones
   - ✅ Valores normalizados entre -1 y 1
   - ✅ Procesamiento por lotes funcional

2. **Hybrid Search Service:**
   - ✅ 15/15 tests pasando
   - ✅ Combinación de resultados de texto y semántica
   - ✅ Filtros por rol funcionando
   - ✅ Scoring ponderado correcto

3. **Cobertura:**
   - ✅ >90% en servicios core
   - ✅ Manejo completo de errores
   - ✅ Todos los métodos públicos testados

### **Comandos de verificación rápida:**
```bash
# Verificación completa en un comando
pytest tests/unit/test_openai_embedding_service.py tests/unit/test_hybrid_search_service.py -v --tb=short

# Resumen de cobertura
pytest tests/unit/ --cov=app.infrastructure.services --cov-report=term --tb=no -q
```

---

## 🐛 **TROUBLESHOOTING**

### **Problemas comunes:**

1. **ModuleNotFoundError**: 
   - Verificar que el venv esté activado
   - Instalar dependencias: `pip install -r requirements.txt`

2. **ImportError en tests**:
   - Ejecutar desde el directorio raíz de kbservice
   - Verificar estructura de carpetas

3. **Timeout en tests con API**:
   - Verificar conexión a internet
   - Aumentar timeout en settings si es necesario

4. **Tests fallan por configuración**:
   - Verificar que `settings.EMBEDDING_DIMENSION = 1536`
   - Confirmar configuraciones en `app/config.py`

---

## ✅ **CRITERIOS DE ÉXITO**

Para considerar los servicios core completamente funcionales:

- [ ] Todos los tests unitarios pasan (27/27)
- [ ] Cobertura >90% en servicios core
- [ ] Embeddings generados correctamente (mock y real)
- [ ] Búsqueda híbrida combina resultados apropiadamente
- [ ] Manejo robusto de errores implementado
- [ ] Configuraciones avanzadas funcionando
- [ ] Performance adecuado en procesamiento por lotes

**Estado actual: ✅ COMPLETADO**
