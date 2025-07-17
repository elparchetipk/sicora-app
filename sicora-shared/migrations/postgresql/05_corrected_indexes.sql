-- Índices corregidos para las tablas existentes en scheduleservice_schema

-- Índices adicionales para tabla schedules (algunos ya existen)
CREATE INDEX IF NOT EXISTS idx_schedules_start_date ON scheduleservice_schema.schedules USING btree (start_date);
CREATE INDEX IF NOT EXISTS idx_schedules_end_date ON scheduleservice_schema.schedules USING btree (end_date);
CREATE INDEX IF NOT EXISTS idx_schedules_day_of_week ON scheduleservice_schema.schedules USING btree (day_of_week);
CREATE INDEX IF NOT EXISTS idx_schedules_start_time ON scheduleservice_schema.schedules USING btree (start_time);
CREATE INDEX IF NOT EXISTS idx_schedules_active ON scheduleservice_schema.schedules USING btree (is_active);
CREATE INDEX IF NOT EXISTS idx_schedules_status ON scheduleservice_schema.schedules USING btree (status);

-- Índices compuestos para consultas frecuentes y paginación
CREATE INDEX IF NOT EXISTS idx_schedules_group_start_date ON scheduleservice_schema.schedules USING btree (academic_group_id, start_date);
CREATE INDEX IF NOT EXISTS idx_schedules_instructor_start_date ON scheduleservice_schema.schedules USING btree (instructor_id, start_date);
CREATE INDEX IF NOT EXISTS idx_schedules_venue_start_date ON scheduleservice_schema.schedules USING btree (venue_id, start_date);
CREATE INDEX IF NOT EXISTS idx_schedules_date_range ON scheduleservice_schema.schedules USING btree (start_date, end_date);

-- Índice para consultas de horarios por día de la semana y hora
CREATE INDEX IF NOT EXISTS idx_schedules_day_time ON scheduleservice_schema.schedules USING btree (day_of_week, start_time);

-- Verificar si existen otras tablas y crear índices apropiados
-- (Este script se puede ejecutar de forma segura múltiples veces)
