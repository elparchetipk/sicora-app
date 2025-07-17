# 🔧 Scripts de SICORA Backend Python

## 📋 Scripts Disponibles

Esta carpeta contiene todos los scripts de automatización y utilidades específicos del backend Python SICORA.

### 🐍 Scripts de Python

- test_integration.sh
- test_integration_simple.sh
- validate-python313.py
- verify-doc-structure.sh

### 🧪 Scripts de Testing

- Scripts de testing de integración
- Scripts de pruebas de servicios
- Scripts de verificación de calidad

### 📊 Reportes Generados

Los scripts generan reportes automáticos en `_docs/reportes/`

### 🛠️ Uso

```bash
# Verificar estructura de documentación
./scripts/verify-doc-structure.sh verify

# Organizar archivos automáticamente
./scripts/verify-doc-structure.sh organize

# Ejecutar tests de integración
./scripts/test_integration.sh
```

### 🚀 Scripts de Desarrollo

```bash
# Iniciar todos los servicios
./start_services.sh

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---
*Mantén esta documentación actualizada cuando agregues nuevos scripts.*
