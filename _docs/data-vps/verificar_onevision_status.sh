#!/bin/bash
# Script para verificar el estado de la base de datos OneVision

echo "🔍 VERIFICACIÓN ESTADO BASE DE DATOS ONEVISION"
echo "=============================================="

# Función para ejecutar consultas SQL
run_sql() {
    docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "$1" 2>/dev/null
}

echo ""
echo "📊 CONTEO PRINCIPAL DE TABLAS:"
echo "------------------------------"

# Verificar usuarios por rol
echo "👥 USUARIOS POR ROL:"
run_sql "SELECT role, COUNT(*) as cantidad FROM userservice_schema.users WHERE deleted_at IS NULL GROUP BY role ORDER BY role;"

echo ""
echo "🏢 INFRAESTRUCTURA:"
run_sql "SELECT 'venues' as tabla, COUNT(*) as cantidad FROM scheduleservice_schema.venues WHERE deleted_at IS NULL
UNION ALL
SELECT 'academic_programs', COUNT(*) FROM scheduleservice_schema.academic_programs WHERE deleted_at IS NULL
UNION ALL
SELECT 'academic_groups', COUNT(*) FROM scheduleservice_schema.academic_groups WHERE deleted_at IS NULL
UNION ALL
SELECT 'schedules', COUNT(*) FROM scheduleservice_schema.schedules WHERE deleted_at IS NULL;"

echo ""
echo "⏰ HORARIOS POR JORNADA:"
run_sql "SELECT
    ag.shift as jornada,
    COUNT(s.id) as horarios_asignados
FROM scheduleservice_schema.academic_groups ag
LEFT JOIN scheduleservice_schema.schedules s ON ag.id = s.academic_group_id AND s.deleted_at IS NULL
WHERE ag.deleted_at IS NULL AND ag.status = 'ACTIVE'
GROUP BY ag.shift
ORDER BY ag.shift;"

echo ""
echo "📅 REGISTROS DE ASISTENCIA:"
if run_sql "\dt attendanceservice_schema.attendance_records" | grep -q "attendance_records"; then
    run_sql "SELECT COUNT(*) as total_asistencias FROM attendanceservice_schema.attendance_records;"
else
    echo "❌ Tabla de asistencia no encontrada"
fi

echo ""
echo "🔄 ESTADO DE CONEXIÓN:"
echo "Base de datos: onevision_testing"
echo "Contenedor: sicora-postgres"
echo "Usuario: sicora_user"
echo "Fecha verificación: $(date '+%Y-%m-%d %H:%M:%S')"
