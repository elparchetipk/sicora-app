# 🚀 GUÍA RÁPIDA: Base de Datos OneVision VPS

## ⚡ Ejecución Automática (FASES 1-3)

### Opción A: Script Automatizado

```bash
# Ejecutar script automatizado para FASES 1-3
cd /home/epti/Documentos/epti-dev/sicora-app/_docs/data-vps
./ejecutar_onevision_vps.sh
```

**¿Qué hace el script?**

- ✅ Crea base de datos `onevision_testing` independiente
- ✅ Crea todos los esquemas necesarios
- ✅ FASE 1: Tabla `users` + 1 coordinador
- ✅ FASE 2: Tabla `venues` + 100 aulas (50 Calle 52, 50 Fontibón)
- ✅ FASE 3: Tabla `academic_programs` + 20 programas

### Opción B: Ejecución Manual

```bash
# Conectar a VPS
ssh fedora@TU_IP_VPS

# Conectar a PostgreSQL
docker exec -it sicora-postgres psql -U sicora_user -d sicora_dev

# Crear base de datos independiente
CREATE DATABASE onevision_testing;
\c onevision_testing;

# Continuar con PLAN_EJECUCION_VPS_ONEVISION.md paso a paso...
```

## 📊 FASES 4-8: Ejecución Manual Requerida

Después de completar FASES 1-3, continuar con:

- **FASE 4**: 100 Fichas (`academic_groups`)
- **FASE 5**: 100 Instructores
- **FASE 6**: ~2,750 Aprendices (25-30 por ficha)
- **FASE 7**: ~375 Horarios únicos
- **FASE 8**: ~206,250 Registros de asistencia

**📖 Scripts detallados en:** `PLAN_EJECUCION_VPS_ONEVISION.md`

## 🔍 Verificación Rápida

```bash
# Conectar a la nueva base de datos
docker exec -it sicora-postgres psql -U sicora_user -d onevision_testing

# Verificar todas las tablas creadas
SELECT
    schemaname,
    tablename,
    COALESCE(n_tup_ins, 0) as registros
FROM pg_stat_user_tables
ORDER BY schemaname, tablename;
```

## 🎯 Resultado Final Esperado

- **1 Coordinador** ✅
- **100 Venues** ✅
- **20 Programas** ✅
- **100 Fichas** (FASE 4)
- **100 Instructores** (FASE 5)
- **~2,750 Aprendices** (FASE 6)
- **~375 Horarios** (FASE 7)
- **~206,250 Registros Asistencia** (FASE 8)

## ⚠️ Notas Importantes

1. **Base de Datos Independiente**: `onevision_testing` (separada de SICORA)
2. **Redis**: Se puebla automáticamente al iniciar servicios
3. **Verificación**: Validar cada fase antes de continuar
4. **Backups**: Considerar respaldo después de cada fase importante

## 🛠️ Troubleshooting

### Error: Contenedor no encontrado

```bash
# Verificar contenedores activos
docker ps | grep postgres

# Iniciar si está detenido
cd ~/sicora-backend && docker-compose up -d postgres
```

### Error: Base de datos ya existe

```bash
# Eliminar base de datos existente
docker exec -it sicora-postgres psql -U sicora_user -d sicora_dev -c "DROP DATABASE IF EXISTS onevision_testing;"
```

### Error: Permisos insuficientes

```bash
# Verificar permisos del script
ls -la ejecutar_onevision_vps.sh

# Dar permisos si es necesario
chmod +x ejecutar_onevision_vps.sh
```

---

**📞 ¿Listo para ejecutar?**

- Ejecuta `./ejecutar_onevision_vps.sh` para empezar
- O consulta `PLAN_EJECUCION_VPS_ONEVISION.md` para ejecución manual completa
