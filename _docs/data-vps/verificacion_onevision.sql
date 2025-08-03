-- Consulta de verificación OneVision
\c onevision_testing;

\echo '🔍 VERIFICACIÓN BASE DE DATOS ONEVISION'
\echo '======================================'

\echo ''
\echo '👥 USUARIOS POR ROL:'
SELECT role, COUNT(*) as cantidad
FROM userservice_schema.users
WHERE deleted_at IS NULL
GROUP BY role
ORDER BY role;

\echo ''
\echo '🏢 INFRAESTRUCTURA:'
SELECT 'venues' as tabla, COUNT(*) as cantidad
FROM scheduleservice_schema.venues
WHERE deleted_at IS NULL
UNION ALL
SELECT 'academic_programs', COUNT(*)
FROM scheduleservice_schema.academic_programs
WHERE deleted_at IS NULL
UNION ALL
SELECT 'academic_groups', COUNT(*)
FROM scheduleservice_schema.academic_groups
WHERE deleted_at IS NULL
UNION ALL
SELECT 'schedules', COUNT(*)
FROM scheduleservice_schema.schedules
WHERE deleted_at IS NULL;

\echo ''
\echo '⏰ HORARIOS POR JORNADA:'
SELECT
    ag.shift as jornada,
    COUNT(s.id) as horarios_asignados
FROM scheduleservice_schema.academic_groups ag
LEFT JOIN scheduleservice_schema.schedules s ON ag.id = s.academic_group_id AND s.deleted_at IS NULL
WHERE ag.deleted_at IS NULL AND ag.status = 'ACTIVE'
GROUP BY ag.shift
ORDER BY ag.shift;

\echo ''
\echo '🗓️ EJEMPLO DE HORARIOS:'
SELECT
    ag.name as ficha,
    ag.shift as jornada,
    s.day_of_week as dia,
    s.start_time as inicio,
    s.end_time as fin
FROM scheduleservice_schema.academic_groups ag
JOIN scheduleservice_schema.schedules s ON ag.id = s.academic_group_id
WHERE ag.deleted_at IS NULL AND s.deleted_at IS NULL
ORDER BY ag.name, s.day_of_week, s.start_time
LIMIT 10;
