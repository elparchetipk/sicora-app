# 🔗 Integración con Modelos Compartidos - ProjectEval Service

## 📋 Resumen

Este documento describe cómo ProjectEval Service consume e integra modelos compartidos del repositorio `sicora-shared`, siguiendo el patrón establecido para centralización de esquemas y contratos.

---

## 🏗️ Arquitectura de Modelos Compartidos

### **Ubicaciones:**

```
sicora-shared/
├── schemas/
│   ├── entities/                    # Entidades Pydantic base
│   │   ├── project.py              # ✅ Usado en ProjectEval
│   │   ├── stakeholder.py          # ✅ Usado en ProjectEval
│   │   ├── evaluation.py           # ✅ Usado en ProjectEval
│   │   └── user.py                 # ✅ Referenciado via evaluator_id
│   ├── requests/                   # DTOs de entrada
│   │   ├── project_create.py       # ✅ Usado en ProjectEval
│   │   ├── stakeholder_create.py   # ✅ Usado en ProjectEval
│   │   └── evaluation_create.py    # ✅ Usado en ProjectEval
│   └── responses/                  # DTOs de salida
│       ├── project_response.py     # ✅ Usado en ProjectEval
│       ├── stakeholder_response.py # ✅ Usado en ProjectEval
│       └── evaluation_response.py  # ✅ Usado en ProjectEval
└── api-contracts/
    ├── project.openapi.yaml        # ✅ Contrato para proyectos
    ├── stakeholder.openapi.yaml    # ✅ Contrato para stakeholders
    └── evaluation.openapi.yaml     # ✅ Contrato para evaluaciones
```

---

## 🔧 Configuración de Consumo

### **1. Importación en projectevalservice:**

```python
# app/domain/entities/project.py
from sicora_shared.schemas.entities.project import ProjectEntity

# app/application/dtos/project_dtos.py
from sicora_shared.schemas.requests.project_create import ProjectCreateRequest
from sicora_shared.schemas.responses.project_response import ProjectResponse

# app/infrastructure/database/models/project_model.py
# Modelo SQLAlchemy independiente, alineado con ProjectEntity
```

### **2. Mapeo Entity ↔ Model:**

```python
# app/infrastructure/mappers/project_mapper.py
from app.domain.entities.project import ProjectEntity
from app.infrastructure.database.models.project_model import ProjectModel

class ProjectMapper:
    @staticmethod
    def to_entity(model: ProjectModel) -> ProjectEntity:
        return ProjectEntity(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            project_type=model.project_type,
            # ... mapping fields
        )

    @staticmethod
    def to_model(entity: ProjectEntity) -> ProjectModel:
        return ProjectModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            # ... mapping fields
        )
```

### **3. Validación de Contratos:**

Los contratos OpenAPI en `sicora-shared/api-contracts/` definen:

- Estructura exacta de requests/responses
- Códigos de estado HTTP
- Formatos de error
- Documentación de endpoints

---

## 📊 Flujo de Datos

### **Request Flow:**

```
1. API Request → ProjectCreateRequest (sicora-shared)
2. DTO Validation → Business Logic
3. Entity Creation → ProjectEntity (sicora-shared)
4. Persistence → ProjectModel (local SQLAlchemy)
5. Response → ProjectResponse (sicora-shared)
```

### **Query Flow:**

```
1. Database Query → ProjectModel (local)
2. Mapping → ProjectEntity (sicora-shared)
3. Business Logic → Domain Services
4. Response → ProjectResponse (sicora-shared)
```

---

## 🔄 Sincronización con Shared Models

### **Workflow de Actualización:**

1. **Cambios en sicora-shared** → Notificación a equipos
2. **Review de Breaking Changes** → Análisis de impacto
3. **Update en projectevalservice** → Ajuste de mappers
4. **Testing de Integración** → Validación end-to-end
5. **Deploy Coordinado** → Todos los servicios

### **Comandos de Sincronización:**

```bash
# Actualizar referencia a sicora-shared
git submodule update --remote sicora-shared

# Verificar compatibilidad
make validate-shared-models

# Ejecutar tests de integración
make test-integration
```

---

## 🧪 Testing de Modelos Compartidos

### **Tests de Compatibilidad:**

```python
# tests/integration/test_shared_models.py
def test_project_entity_compatibility():
    """Verifica que ProjectEntity funcione correctamente"""
    from sicora_shared.schemas.entities.project import ProjectEntity

    # Test de creación
    project = ProjectEntity(
        id="test-id",
        title="Test Project",
        description="Test Description",
        project_type="FORMATIVE",
        status="IDEA_PROPOSAL"
    )

    assert project.id == "test-id"
    assert project.is_valid()

def test_project_model_entity_mapping():
    """Verifica mapeo bidireccional Entity ↔ Model"""
    # Test de conversión Model → Entity → Model
    pass
```

### **Validación de Contratos API:**

```bash
# Verificar que los endpoints cumplan contratos OpenAPI
swagger-codegen validate -i sicora-shared/api-contracts/project.openapi.yaml
```

---

## 📈 Beneficios de la Centralización

### **✅ Ventajas:**

- **Consistencia:** Todos los servicios usan mismos DTOs
- **Versionado:** Control centralizado de cambios
- **Documentación:** Contratos OpenAPI unificados
- **Testing:** Validación automática de compatibilidad
- **Desarrollo:** Menos duplicación de código

### **⚠️ Consideraciones:**

- **Dependencia:** Cambios en shared afectan múltiples servicios
- **Coordinación:** Deploy sincronizado requerido
- **Versionado:** Estrategia de backward compatibility

---

## 🔧 Comandos de Desarrollo

### **Makefile Integrado:**

```bash
# Validar modelos compartidos
make validate-shared-models

# Actualizar referencia a sicora-shared
make update-shared

# Test de integración completa
make test-integration

# Verificar compatibilidad de contratos
make validate-contracts
```

### **Scripts de Sincronización:**

```bash
# sync-shared-models.sh
#!/bin/bash
git submodule update --remote sicora-shared
python scripts/validate_shared_compatibility.py
make test-integration
```

---

## 📚 Referencias

- **Repo Principal:** `sicora-shared/`
- **Documentación:** `sicora-shared/README.md`
- **Contratos API:** `sicora-shared/api-contracts/`
- **Historial de Cambios:** `sicora-shared/CHANGELOG.md`

Este patrón asegura que ProjectEval Service mantenga consistencia con el ecosistema SICORA mientras mantiene su autonomía operacional.
