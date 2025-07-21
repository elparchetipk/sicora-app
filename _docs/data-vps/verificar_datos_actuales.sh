#!/bin/bash

echo "🔍 VERIFICACIÓN DE DATOS ONEVISION - $(date)"
echo "=============================================="

# Verificar conexión a la base de datos
echo "📊 VERIFICANDO CONTENIDO DE LA BASE DE DATOS..."

# Contar usuarios por rol
echo "👥 USUARIOS:"
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "SELECT 'Coordinadores: ' || COUNT(*) FROM userservice_schema.users WHERE role = 'ADMIN'"
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "SELECT 'Instructores: ' || COUNT(*) FROM userservice_schema.users WHERE role = 'INSTRUCTOR'"
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "SELECT 'Aprendices: ' || COUNT(*) FROM userservice_schema.users WHERE role = 'APPRENTICE'"

# Contar infraestructura
echo ""
echo "🏢 INFRAESTRUCTURA:"
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "SELECT 'Venues/Aulas: ' || COUNT(*) FROM scheduleservice_schema.venues"
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "SELECT 'Programas: ' || COUNT(*) FROM scheduleservice_schema.academic_programs"
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "SELECT 'Fichas: ' || COUNT(*) FROM scheduleservice_schema.academic_groups"

# Verificar horarios y asistencia si existen
echo ""
echo "⏰ OPERACIONES:"
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "SELECT 'Horarios: ' || COUNT(*) FROM scheduleservice_schema.schedules" 2>/dev/null || echo "Horarios: Tabla no existe"

# Verificar tabla de asistencia
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -t -c "SELECT 'Asistencias: ' || COUNT(*) FROM attendanceservice_schema.attendance_records" 2>/dev/null || echo "Asistencias: Tabla no existe"

echo ""
echo "✅ VERIFICACIÓN COMPLETADA"
