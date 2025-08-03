#!/bin/bash

# Script rápido para verificar el estado actual
echo "🔍 VERIFICACIÓN RÁPIDA - BASE DE DATOS VPS"
echo "=========================================="
echo "Fecha: $(date)"
echo ""

# Verificar conexión y esquemas
echo "📊 Verificando esquemas en onevision_testing..."
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -c "
SELECT
    schemaname,
    COUNT(*) as num_tables
FROM pg_tables
WHERE schemaname LIKE '%service%'
GROUP BY schemaname
ORDER BY schemaname;
"

echo ""
echo "📋 Verificando tablas de EvalinService..."
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -c "
SELECT tablename
FROM pg_tables
WHERE schemaname = 'evalinservice_schema'
ORDER BY tablename;
"

echo ""
echo "🎯 Verificando datos en EvalinService..."
docker exec sicora-postgres psql -U sicora_user -d onevision_testing -c "
SELECT
    'questions' as tabla,
    COUNT(*) as registros
FROM evalinservice_schema.questions
UNION ALL
SELECT
    'evaluations' as tabla,
    COUNT(*) as registros
FROM evalinservice_schema.evaluations
UNION ALL
SELECT
    'responses' as tabla,
    COUNT(*) as registros
FROM evalinservice_schema.responses;
" 2>/dev/null || echo "❌ Error: Tablas no existen o sin datos"

echo ""
echo "✅ Verificación completada"
