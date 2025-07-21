## 📋 OneVision VPS - Base de Datos de Prueba

Documentación completa para la creación de una base de datos independiente de OneVision en el VPS Hostinger:

### 🚀 Ejecución Rápida

- **[GUIA_RAPIDA_ONEVISION.md](./GUIA_RAPIDA_ONEVISION.md)** - Comandos directos para ejecución inmediata
- **[ejecutar_onevision_vps.sh](./ejecutar_onevision_vps.sh)** - Script automatizado (FASES 1-3)

### 📊 Planificación Detallada

- **[PLAN_EJECUCION_VPS_ONEVISION.md](./PLAN_EJECUCION_VPS_ONEVISION.md)** - Plan completo 8 fases con scripts SQL
- **[RESUMEN_EJECUTIVO_ONEVISION.md](./RESUMEN_EJECUTIVO_ONEVISION.md)** - Estado actual y próximos pasos

### 📝 Requisitos Base

- **[data-requirements.md](./data-requirements.md)** - Especificaciones técnicas y requisitos funcionales

### 🎯 Objetivo

Crear una base de datos `onevision_testing` independiente con:

- 1 coordinador, 100 venues, 20 programas, 100 fichas
- 100 instructores, ~2,750 aprendices
- ~375 horarios únicos, ~206,250 registros de asistencia

### ▶️ Próximo Paso

```bash
cd _docs/data-vps
./ejecutar_onevision_vps.sh
```
