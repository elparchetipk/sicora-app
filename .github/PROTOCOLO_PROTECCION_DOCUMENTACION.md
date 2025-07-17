# 🛡️ PROTOCOLO DE PROTECCIÓN ESTRICTA DE DOCUMENTACIÓN SICORA

**FECHA:** 4 de julio de 2025  
**VERSIÓN:** 1.0 - PROTECCIÓN CRÍTICA  
**AUTORIDAD:** Protocolo de Seguridad Documental

## 🚨 REGLAS CRÍTICAS - CUMPLIMIENTO OBLIGATORIO

### ❌ PROHIBICIONES ABSOLUTAS:

1. **NUNCA** eliminar documentación existente sin autorización humana explícita
2. **NUNCA** sobrescribir archivos `.md` completos sin verificación previa
3. **NUNCA** mover archivos sin crear backup automático
4. **NUNCA** usar herramientas destructivas (`rm`, `mv` sin backup) en documentación
5. **NUNCA** ignorar este protocolo bajo ninguna circunstancia

### ✅ PROCEDIMIENTOS OBLIGATORIOS:

1. **BACKUP AUTOMÁTICO** antes de cualquier modificación
2. **VERIFICACIÓN DE CONTENIDO** antes de cualquier operación
3. **AUTORIZACIÓN HUMANA** para cambios estructurales
4. **VALIDACIÓN POST-CAMBIO** después de cualquier modificación
5. **REGISTRO DE AUDITORÍA** de todas las operaciones

## 🔒 SISTEMA DE PROTECCIÓN DE DOCUMENTACIÓN

### Nivel 1: Documentos CRÍTICOS (Máxima Protección)

Requieren autorización humana explícita para cualquier cambio:

```
_docs/mcp/GUIA_MCP_PRINCIPIANTES.md
_docs/mcp/CHECKLIST_MCP_PRINCIPIANTES.md
_docs/mcp/RESUMEN_MCP_PRINCIPIANTES.md
_docs/guias/FORMATO_CSV_PROGRAMAS_FORMACION.md
_docs/guias/ESTRATEGIA_POSTMAN_SICORA_EDUCATIVA.md
_docs/reportes/CONTEO_ENDPOINTS_BACKEND_SICORA.md
_docs/reportes/ANALISIS_ENDPOINTS_COMPLETADO.md
```

### Nivel 2: Documentos IMPORTANTES (Alta Protección)

Requieren backup automático antes de modificación:

```
**/README.md
**/_docs/**/*.md
scripts/**/*.md
```

### Nivel 3: Documentos ESTRUCTURALES (Protección Estándar)

Sujetos a validación post-cambio:

```
.github/**/*.md
**/configuracion/**/*.md
```

## 🛠️ HERRAMIENTAS DE PROTECCIÓN

### 1. Script de Backup Automático

```bash
#!/bin/bash
# scripts/backup-docs.sh

backup_doc() {
    local file="$1"
    local backup_dir="/backup/docs/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    cp "$file" "$backup_dir/"
    echo "✅ BACKUP: $file → $backup_dir/"
}
```

### 2. Script de Verificación de Integridad

```bash
#!/bin/bash
# scripts/verify-doc-integrity.sh

verify_doc() {
    local file="$1"
    if [ ! -s "$file" ]; then
        echo "🚨 ALERTA: $file está vacío o no existe"
        return 1
    fi

    local line_count=$(wc -l < "$file")
    if [ "$line_count" -lt 10 ]; then
        echo "⚠️  ADVERTENCIA: $file tiene menos de 10 líneas"
    fi

    echo "✅ VERIFICADO: $file ($line_count líneas)"
    return 0
}
```

### 3. Hook de Protección Pre-Modificación

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Verificar documentación antes de commit
./scripts/verify-doc-integrity.sh
if [ $? -ne 0 ]; then
    echo "🚨 COMMIT BLOQUEADO: Documentación corrupta detectada"
    exit 1
fi
```

## 📋 PROTOCOLO DE AUTORIZACIÓN HUMANA

### Para Cambios Críticos:

1. **SOLICITUD**: Describir el cambio requerido
2. **JUSTIFICACIÓN**: Explicar por qué es necesario
3. **IMPACTO**: Evaluar efectos en documentación existente
4. **BACKUP**: Crear backup completo antes de proceder
5. **AUTORIZACIÓN**: Obtener aprobación humana explícita
6. **EJECUCIÓN**: Realizar cambio con monitoreo
7. **VALIDACIÓN**: Verificar integridad post-cambio
8. **REGISTRO**: Documentar la operación

### Frases de Autorización Requeridas:

- "AUTORIZO MODIFICACIÓN DOCUMENTAL"
- "CONFIRMO BACKUP REALIZADO"
- "APRUEBO CAMBIO ESTRUCTURAL"
- "VALIDO INTEGRIDAD POST-CAMBIO"

## 🔍 MONITOREO CONTINUO

### Verificaciones Automáticas:

```bash
# Ejecutar cada hora
0 * * * * /sicora-app/scripts/verify-doc-integrity.sh

# Backup diario
0 2 * * * /sicora-app/scripts/backup-docs.sh

# Reporte semanal
0 9 * * 1 /sicora-app/scripts/doc-health-report.sh
```

### Alertas Críticas:

- 🚨 Documento vacío detectado
- ⚠️ Pérdida de contenido significativa
- 📉 Reducción drástica de líneas
- 🔴 Fallo en backup automático

## 📊 REGISTRO DE AUDITORÍA

Todas las operaciones documentales deben registrarse:

```
TIMESTAMP | OPERACIÓN | ARCHIVO | USUARIO | ESTADO | OBSERVACIONES
2025-07-04T15:30:00 | MODIFICAR | GUIA_MCP.md | COPILOT | BLOQUEADO | Sin autorización
2025-07-04T15:31:00 | BACKUP | GUIA_MCP.md | SISTEMA | EXITOSO | Backup creado
2025-07-04T15:32:00 | MODIFICAR | GUIA_MCP.md | HUMANO | AUTORIZADO | Cambio aprobado
```

## 🚨 PROCEDIMIENTO DE EMERGENCIA

### En caso de pérdida documental:

1. **PARAR** todas las operaciones inmediatamente
2. **EVALUAR** el alcance del daño
3. **RESTAURAR** desde último backup válido
4. **INVESTIGAR** causa raíz del problema
5. **REPORTAR** incidente para prevención futura
6. **REFORZAR** medidas de protección

## ⚖️ RESPONSABILIDADES

### GitHub Copilot / AI Assistant:

- Cumplir estrictamente este protocolo
- Solicitar autorización para cambios críticos
- Crear backups antes de modificaciones
- Verificar integridad post-cambio
- Reportar anomalías inmediatamente

### Usuario Humano:

- Autorizar cambios críticos explícitamente
- Revisar reportes de integridad
- Mantener backups actualizados
- Validar cambios importantes

## 📞 CONTACTO DE EMERGENCIA

Para incidentes críticos de documentación:

- **PROTOCOLO**: Parar operaciones inmediatamente
- **ACCIÓN**: Solicitar intervención humana
- **PRIORIDAD**: Máxima - Protección documental

---

**🛡️ ESTE PROTOCOLO ES VINCULANTE Y DE CUMPLIMIENTO OBLIGATORIO**  
**📝 Cualquier violación debe ser reportada inmediatamente**  
**🔒 La protección documental es CRÍTICA para el proyecto SICORA**
