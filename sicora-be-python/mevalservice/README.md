# MEvalService - Comités de Seguimiento y Evaluación Académico/Disciplinario

**Sistema de Gestión de Comités según Reglamento del Aprendiz Acuerdo 009 de 2024**

## 🎯 Propósito

MEvalService gestiona automáticamente los comités mensuales de seguimiento y evaluación, facilitando:

- 📅 **Programación mensual automática** de comités
- 🏆 **Citación por destacado desempeño** académico/disciplinario
- ⚖️ **Evaluación de incumplimientos** de planes de mejoramiento
- 📋 **Aplicación gradual de sanciones** según reglamento SENA
- ⚖️ **Debido proceso** en todas las decisiones
- 📊 **Alertas tempranas** para intervención preventiva

## 🏗️ Arquitectura

- **Framework**: FastAPI + SQLAlchemy + PostgreSQL 15
- **Puerto**: 8009
- **Esquema DB**: `mevalservice_schema`
- **Arquitectura**: Clean Architecture (4 capas)

```
mevalservice/
├── app/
│   ├── domain/                 # Entidades y reglas de negocio
│   ├── application/            # Casos de uso
│   ├── infrastructure/         # Base de datos y servicios externos
│   └── presentation/           # API REST y schemas
├── tests/
├── alembic/                    # Migraciones de BD
└── requirements.txt
```

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Database
DATABASE_URL=postgresql://meval_user:meval_password@localhost:5432/sicora_db
DB_SCHEMA=mevalservice_schema

# API
API_PORT=8009
API_HOST=0.0.0.0
DEBUG=True

# External Services
USER_SERVICE_URL=http://localhost:8001
SCHEDULE_SERVICE_URL=http://localhost:8003
ATTENDANCE_SERVICE_URL=http://localhost:8004
NOTIFICATION_SERVICE_URL=http://localhost:8011

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Jobs
ENABLE_SCHEDULED_JOBS=True
MONTHLY_ANALYSIS_CRON="0 8 * * 0"  # Domingo 8:00 AM
ALERT_CHECK_CRON="0 */4 * * *"     # Cada 4 horas
```

## 🚀 Instalación y Ejecución

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con valores correctos

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload --port 8009
```

## 📊 Flujo Automático Mensual

### Semana 1: Análisis Automático

- **Domingo 8:00 AM**: Ejecución automática del algoritmo de detección
- Análisis de rendimiento académico del mes anterior
- Identificación de casos para felicitación y evaluación
- Generación de reportes preliminares

### Semana 2: Convocatorias

- Validación de casos por coordinador académico
- Generación automática de convocatorias (8 días anticipación)
- Notificación a aprendices y acudientes

### Semana 3: Sesión del Comité

- Verificación de quórum y apertura formal
- Bloque de felicitaciones por destacado desempeño
- Bloque de evaluaciones por incumplimiento
- Votación formal y documentación de decisiones

### Semana 4: Seguimiento

- Comunicación oficial de decisiones (48 horas máximo)
- Activación de planes de mejoramiento y sanciones
- Actualización de expedientes académicos
- Reporte mensual institucional

## 🔄 Casos de Uso Principales

1. **Programar Comité Mensual**: Programación automática con algoritmos de detección
2. **Citar por Destacado Desempeño**: Identificación automática de excelencia académica
3. **Evaluar Incumplimientos**: Gestión de casos de planes de mejoramiento no cumplidos
4. **Gestionar Apelaciones**: Proceso de segunda instancia conforme al debido proceso

## 📋 Endpoints Principales

```
GET    /api/v1/committees                    # Listar comités
POST   /api/v1/committees                    # Crear comité
GET    /api/v1/committees/{id}               # Obtener comité específico
PUT    /api/v1/committees/{id}               # Actualizar comité

GET    /api/v1/student-cases                 # Listar casos de estudiantes
POST   /api/v1/student-cases                 # Crear caso manual
GET    /api/v1/student-cases/{id}            # Obtener caso específico

GET    /api/v1/improvement-plans             # Listar planes de mejoramiento
POST   /api/v1/improvement-plans             # Crear plan de mejoramiento
PUT    /api/v1/improvement-plans/{id}        # Actualizar cumplimiento

GET    /api/v1/sanctions                     # Listar sanciones
POST   /api/v1/sanctions                     # Aplicar sanción
GET    /api/v1/sanctions/{id}                # Obtener sanción específica

POST   /api/v1/appeals                       # Presentar apelación
GET    /api/v1/appeals/{id}                  # Consultar estado de apelación

POST   /api/v1/analytics/detect-cases        # Ejecutar detección manual
GET    /api/v1/analytics/dashboard           # Dashboard de métricas
GET    /api/v1/analytics/reports/monthly     # Reporte mensual
```

## 🎯 Criterios de Detección Automática

### Destacado Desempeño (Felicitación)

- Calificación promedio ≥ 4.5 en últimos 3 meses
- Cero faltas disciplinarias en período evaluado
- Participación activa en actividades institucionales
- Liderazgo positivo reportado por instructores

### Incumplimiento (Sanción)

- No alcanzar metas de plan de mejoramiento en deadline
- Reincidencia en faltas disciplinarias
- Incumplimiento de compromisos académicos específicos
- Ausentismo injustificado > 20% en período

## 📈 Métricas de Éxito

- **Automatización**: 90% de casos detectados automáticamente
- **Cumplimiento**: 85% de planes de mejoramiento exitosos
- **Oportunidad**: 100% de convocatorias con 8+ días de anticipación
- **Trazabilidad**: 100% de decisiones documentadas oficialmente
- **Debido Proceso**: 0% de apelaciones ganadas por vicios de procedimiento

## 🔗 Integraciones

- **UserService**: Datos de aprendices e instructores
- **ScheduleService**: Calificaciones y rendimiento académico
- **AttendanceService**: Registro de asistencia e inasistencias
- **NotificationService**: Comunicaciones oficiales automáticas

---

**Documentación Técnica Completa:** [rf_mevalservice.md](../../../sicora-docs/_docs/general/rf_mevalservice.md)
