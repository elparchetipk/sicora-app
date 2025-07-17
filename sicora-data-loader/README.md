# 🚀 SICORA Data Loader

Mini-aplicación para cargar datos desde archivos Excel y PDF a la base de datos SICORA.

## 📋 Características

- **Interfaz Web Intuitiva**: Desarrollada con Streamlit
- **Soporte Multi-formato**: Excel (.xlsx, .xls) y PDF
- **Gestión por Microservicios**: Selección automática de esquemas
- **Validación de Datos**: Verificación antes de la carga
- **Logging Completo**: Trazabilidad de todas las operaciones

## 🏗️ Arquitectura

```
sicora-data-loader/
├── app.py                    # Aplicación principal Streamlit
├── config/
│   └── database.py          # Configuración de base de datos
├── models/
│   └── schemas.py           # Mapeo de microservicios y esquemas
├── services/
│   ├── file_processor.py    # Procesamiento de archivos
│   ├── data_validator.py    # Validación de datos
│   └── database_loader.py   # Carga a base de datos
├── utils/
│   └── logger.py           # Sistema de logging
├── requirements.txt         # Dependencias
└── README.md               # Esta documentación
```

## 📊 Microservicios Soportados

| Microservicio          | Esquema                         | Tablas Principales                 |
| ---------------------- | ------------------------------- | ---------------------------------- |
| UserService            | `userservice_schema`            | users, roles, permissions          |
| AttendanceService      | `attendanceservice_schema`      | attendance_records, justifications |
| ScheduleService        | `scheduleservice_schema`        | schedules, groups, venues          |
| KbService              | `kbservice_schema`              | articles, categories, faqs         |
| EvalinService          | `evalinservice_schema`          | questions, questionnaires          |
| AIService              | `aiservice_schema`              | conversations, training_data       |
| MEvalService           | `mevalservice_schema`           | evaluations, committees            |
| ProjectEvalService     | `projectevalservice_schema`     | projects, evaluations              |
| SoftwareFactoryService | `softwarefactoryservice_schema` | projects, teams                    |

## 🚀 Instalación y Uso

### 1. Preparar el Entorno

```bash
cd sicora-data-loader
pip install -r requirements.txt
```

### 2. Configurar Base de Datos

Editar `config/database.py` con los datos de conexión PostgreSQL.

### 3. Ejecutar la Aplicación

```bash
streamlit run app.py
```

### 4. Usar la Interfaz

1. **Seleccionar Microservicio**: Elige el servicio destino
2. **Seleccionar Tabla**: Elige la tabla donde cargar datos
3. **Subir Archivo**: Excel o PDF con los datos
4. **Validar**: Revisa la vista previa y validaciones
5. **Cargar**: Ejecuta la carga de datos

## 📁 Formatos de Archivo Soportados

### Excel (.xlsx, .xls)

- Primera fila debe contener los nombres de columnas
- Datos a partir de la segunda fila
- Columnas deben coincidir con la estructura de la tabla

### PDF

- Tablas extractables con estructura clara
- Se usa `tabula-py` para extracción
- Requiere formato consistente

## 🔧 Configuración

### Variables de Entorno

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sicora_dev
DB_USER=sicora_user
DB_PASSWORD=sicora_password

# Logging
LOG_LEVEL=INFO
LOG_FILE=data_loader.log
```

## 📝 Logging

Todas las operaciones se registran con:

- Timestamp de la operación
- Usuario (si aplica)
- Archivo procesado
- Registros insertados/actualizados
- Errores y excepciones

## 🛡️ Validaciones

- **Estructura**: Verificación de columnas requeridas
- **Tipos de Datos**: Validación de formatos
- **Restricciones**: Claves primarias, únicas, foráneas
- **Integridad**: Verificación antes de inserción

## 🚨 Manejo de Errores

- Validación previa antes de carga
- Transacciones para garantizar consistencia
- Rollback automático en caso de error
- Reportes detallados de errores

## 📈 Casos de Uso

### Carga Inicial de Usuarios

```
1. Seleccionar UserService
2. Seleccionar tabla 'users'
3. Subir Excel con columnas: name, email, document_number, role
4. Validar datos
5. Cargar masivamente
```

### Importación de Horarios

```
1. Seleccionar ScheduleService
2. Seleccionar tabla 'schedules'
3. Subir Excel con horarios del semestre
4. Validar fechas y referencias
5. Cargar datos
```

### Carga de Artículos KB

```
1. Seleccionar KbService
2. Seleccionar tabla 'articles'
3. Subir PDF estructurado o Excel
4. Procesar contenido
5. Cargar al knowledge base
```

## 🔄 Roadmap

- [ ] Soporte para más formatos (CSV, JSON)
- [ ] Carga incremental/actualización
- [ ] Programación de cargas automáticas
- [ ] API REST para cargas programáticas
- [ ] Dashboard de monitoreo de cargas
- [ ] Integración con CI/CD

---

**Desarrollado para el Proyecto SICORA**  
_Carga eficiente y segura de datos multi-microservicio_
