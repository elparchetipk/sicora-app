# 🔧 Scripts de SICORA Frontend

## 📋 Scripts Disponibles

Esta carpeta contiene todos los scripts de automatización y utilidades específicos del frontend SICORA, organizados y documentados para facilitar su uso.

### 📚 Scripts de Documentación

#### `verify-doc-structure.sh`

**Propósito**: Verificar y mantener la estructura organizada de documentación del frontend

**Uso**:

```bash
# Verificar estructura actual
./scripts/verify-doc-structure.sh

# Verificar estructura actual (explícito)
./scripts/verify-doc-structure.sh verify

# Organizar automáticamente archivos mal ubicados
./scripts/verify-doc-structure.sh organize
```

**Funcionalidades**:

- Verifica que solo README.md esté en la raíz del frontend
- Comprueba la estructura de carpetas en `_docs/`
- Organiza automáticamente archivos `.md` según su contenido
- Genera reportes automáticos de estado
- Crea README.md en carpetas nuevas automáticamente

**Categorías de Organización**:

- `integracion/` - Documentación de integración frontend-backend
- `configuracion/` - Configuración, setup y hostinger
- `desarrollo/` - Planes de desarrollo y guías técnicas
- `reportes/` - Reportes de estado y análisis
- `guias/` - Guías de implementación y correcciones
- `diseno/` - Design tokens, branding y UI/UX
- `general/` - Documentación general y miscelánea

### 🎨 Scripts de Desarrollo Frontend

#### Scripts de Build y Deploy

Los scripts de build y deploy específicos del frontend se mantienen en la raíz del proyecto para facilitar el CI/CD:

- `build.sh` - Script de construcción
- `deploy.sh` - Script de despliegue

### 📊 Reportes Generados

Los scripts generan reportes automáticos en:

- `_docs/reports/VERIFICACION_ESTRUCTURA_DOCUMENTACION_FE.md`

### 🔄 Integración con CI/CD

Para integrar con CI/CD, agregar al pipeline:

```yaml
- name: Verificar estructura de documentación
  run: ./scripts/verify-doc-structure.sh verify
```

### 📝 Convenciones de Nomenclatura

Los archivos de documentación siguen estas convenciones:

- `TITULO_DOCUMENTO.md` - Mayúsculas con guiones bajos
- Prefijos por tipo:
  - `INTEGRACION_` - Documentación de integración
  - `CONFIGURACION_` - Configuración y setup
  - `IMPLEMENTACION_` - Implementaciones completadas
  - `GUIA_` - Guías y tutoriales
  - `REPORTE_` - Reportes y análisis
  - `ESTADO_` - Estados y resúmenes

### 🛠️ Mantenimiento

#### Verificación Regular

```bash
# Ejecutar verificación semanal
./scripts/verify-doc-structure.sh verify

# Si hay archivos mal ubicados, organizarlos
./scripts/verify-doc-structure.sh organize
```

#### Agregar Nuevos Scripts

1. Crear script en `scripts/`
2. Hacer ejecutable: `chmod +x scripts/nuevo-script.sh`
3. Documentar en este README.md
4. Agregar a verificación si es necesario

### 🚨 Reglas de Organización

#### PERMITIDO en la raíz:

- `README.md` (único archivo .md permitido)
- `package.json`, `vite.config.ts`, etc. (archivos de configuración)
- Scripts específicos de deploy/build

#### PROHIBIDO en la raíz:

- Archivos `.md` adicionales (van a `_docs/`)
- Scripts de utilidades (van a `scripts/`)

#### ESTRUCTURA REQUERIDA:

```
sicora-app-fe/
├── README.md (único .md en raíz)
├── scripts/
│   ├── README.md
│   └── verify-doc-structure.sh
└── _docs/
    ├── integracion/
    ├── configuracion/
    ├── desarrollo/
    ├── reportes/
    ├── guias/
    ├── diseno/
    └── general/
```

### 🔍 Troubleshooting

#### Error: "Archivos .md encontrados en la raíz"

```bash
# Solución automática
./scripts/verify-doc-structure.sh organize
```

#### Error: "Carpeta \_docs no encontrada"

```bash
# Crear estructura manualmente
mkdir -p _docs/{integracion,configuracion,desarrollo,reportes,guias,diseno,general}
```

#### Error: "README.md faltante en subcarpeta"

El script crea automáticamente README.md en carpetas nuevas.

---

## 📈 Historial de Cambios

### v1.0 (Julio 2025)

- ✅ Creación del sistema de verificación de estructura
- ✅ Organización automática de 25+ archivos .md
- ✅ Integración con estructura principal de SICORA
- ✅ Reportes automáticos de verificación

---

_Mantén esta documentación actualizada cuando agregues nuevos scripts o funcionalidades._
