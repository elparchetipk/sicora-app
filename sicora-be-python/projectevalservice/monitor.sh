#!/bin/bash
# Script de monitoreo de rendimiento para ProjectEval Service

echo "📊 Monitoreo de Rendimiento - ProjectEval Service"
echo "=================================================="
echo ""

# Verificar conexión
if ! docker exec sicora_postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "❌ Error: No se puede conectar a PostgreSQL"
    exit 1
fi

echo "📈 Estadísticas de Tablas:"
echo "-------------------------"
docker exec sicora_postgres psql -U postgres -d sicora_dev -c "
SELECT 
    schemaname || '.' || tablename as tabla,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    seq_scan as table_scans,
    idx_scan as index_scans,
    CASE 
        WHEN seq_scan > 0 THEN ROUND(seq_tup_read::decimal / seq_scan, 2)
        ELSE 0 
    END as avg_seq_read
FROM pg_stat_user_tables 
WHERE schemaname = 'projectevalservice_schema'
ORDER BY schemaname, tablename;
"

echo ""
echo "🔍 Uso de Índices:"
echo "------------------"
docker exec sicora_postgres psql -U postgres -d sicora_dev -c "
SELECT 
    schemaname || '.' || tablename as tabla,
    indexname,
    idx_scan as usage_count,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE schemaname = 'projectevalservice_schema'
ORDER BY idx_scan DESC;
"

echo ""
echo "💾 Tamaño de Tablas:"
echo "--------------------"
docker exec sicora_postgres psql -U postgres -d sicora_dev -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size
FROM pg_tables 
WHERE schemaname = 'projectevalservice_schema'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"

echo ""
echo "⚠️ Alertas de Rendimiento:"
echo "-------------------------"

# Verificar scans secuenciales excesivos
SEQ_SCANS=$(docker exec sicora_postgres psql -U postgres -d sicora_dev -t -c "
SELECT COALESCE(SUM(seq_scan), 0) 
FROM pg_stat_user_tables 
WHERE schemaname = 'projectevalservice_schema';
" | tr -d ' ')

if [ "$SEQ_SCANS" -gt 1000 ]; then
    echo "⚠️ ALERTA: Demasiados sequential scans ($SEQ_SCANS). Considerar añadir índices."
else
    echo "✅ Sequential scans normales ($SEQ_SCANS)"
fi

# Verificar índices no utilizados
UNUSED_INDEXES=$(docker exec sicora_postgres psql -U postgres -d sicora_dev -t -c "
SELECT COUNT(*) 
FROM pg_stat_user_indexes 
WHERE schemaname = 'projectevalservice_schema' AND idx_scan = 0;
" | tr -d ' ')

if [ "$UNUSED_INDEXES" -gt 0 ]; then
    echo "⚠️ ALERTA: $UNUSED_INDEXES índices no utilizados detectados"
    docker exec sicora_postgres psql -U postgres -d sicora_dev -c "
    SELECT tablename, indexname 
    FROM pg_stat_user_indexes 
    WHERE schemaname = 'projectevalservice_schema' AND idx_scan = 0;
    "
else
    echo "✅ Todos los índices están siendo utilizados"
fi

echo ""
echo "📊 Resumen de Esquema:"
echo "---------------------"
docker exec sicora_postgres psql -U postgres -d sicora_dev -c "
SELECT 
    'Tables' as type, COUNT(*) as count
FROM information_schema.tables 
WHERE table_schema = 'projectevalservice_schema' AND table_type = 'BASE TABLE'
UNION ALL
SELECT 
    'Indexes' as type, COUNT(*) as count
FROM pg_indexes 
WHERE schemaname = 'projectevalservice_schema'
UNION ALL
SELECT 
    'ENUMs' as type, COUNT(*) as count
FROM pg_type t 
JOIN pg_namespace n ON t.typnamespace = n.oid
WHERE n.nspname = 'projectevalservice_schema' AND t.typtype = 'e';
"

echo ""
echo "✅ Monitoreo completado - $(date)"
