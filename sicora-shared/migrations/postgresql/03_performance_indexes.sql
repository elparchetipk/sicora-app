-- Índices optimizados para SICORA - Mejora de rendimiento y paginación
-- Ejecutar después de crear las tablas con Alembic

-- ============================================
-- USERSERVICE SCHEMA - Índices de usuarios
-- ============================================

-- Índices para tabla users (userservice_schema.users)
-- Búsquedas frecuentes: login (email/documento), filtros por rol, estado
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON userservice_schema.users (email);
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email_unique ON userservice_schema.users (email) WHERE is_active = true;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_document ON userservice_schema.users (document_number);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_role ON userservice_schema.users (role);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_active ON userservice_schema.users (is_active);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_created_at ON userservice_schema.users (created_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_last_login ON userservice_schema.users (last_login_at DESC) WHERE last_login_at IS NOT NULL;

-- Índice compuesto para paginación eficiente por rol
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_role_created ON userservice_schema.users (role, created_at DESC);

-- ============================================
-- SCHEDULESERVICE SCHEMA - Índices de horarios
-- ============================================

-- Índices para tabla schedules
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_schedules_date ON scheduleservice_schema.schedules (schedule_date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_schedules_ficha ON scheduleservice_schema.schedules (ficha_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_schedules_instructor ON scheduleservice_schema.schedules (instructor_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_schedules_ambiente ON scheduleservice_schema.schedules (ambiente_id);

-- Índices compuestos para consultas frecuentes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_schedules_ficha_date ON scheduleservice_schema.schedules (ficha_id, schedule_date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_schedules_instructor_date ON scheduleservice_schema.schedules (instructor_id, schedule_date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_schedules_date_range ON scheduleservice_schema.schedules (schedule_date, start_time, end_time);

-- ============================================
-- ATTENDANCESERVICE SCHEMA - Índices de asistencia
-- ============================================

-- Índices para tabla attendance_records
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attendance_student_date ON attendanceservice_schema.attendance_records (student_id, date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attendance_ficha_date ON attendanceservice_schema.attendance_records (ficha_id, date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attendance_status ON attendanceservice_schema.attendance_records (status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attendance_date_desc ON attendanceservice_schema.attendance_records (date DESC);

-- Índice para estadísticas y reportes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attendance_student_status_date ON attendanceservice_schema.attendance_records (student_id, status, date DESC);

-- Índices para tabla justifications
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_justifications_student ON attendanceservice_schema.justifications (student_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_justifications_status ON attendanceservice_schema.justifications (status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_justifications_submitted ON attendanceservice_schema.justifications (submitted_at DESC);

-- ============================================
-- EVALINSERVICE SCHEMA - Índices de evaluaciones
-- ============================================

-- Índices para tabla evaluations
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_evaluations_instructor ON evalinservice_schema.evaluations (instructor_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_evaluations_evaluator ON evalinservice_schema.evaluations (evaluator_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_evaluations_period ON evalinservice_schema.evaluations (evaluation_period);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_evaluations_status ON evalinservice_schema.evaluations (status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_evaluations_created ON evalinservice_schema.evaluations (created_at DESC);

-- Índice compuesto para consultas de periodo
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_evaluations_instructor_period ON evalinservice_schema.evaluations (instructor_id, evaluation_period);

-- ============================================
-- ÍNDICES GENERALES PARA PAGINACIÓN
-- ============================================

-- Estos índices mejoran las consultas con LIMIT/OFFSET
-- Se crean después de que las tablas existan mediante migraciones

-- Nota: Los índices CONCURRENTLY permiten creación sin bloquear la tabla
-- Remover IF NOT EXISTS si hay conflictos en recreación
