-- Índices inmediatos para tablas existentes en scheduleservice_schema

-- Índices para tabla schedules (consultas más frecuentes)
CREATE INDEX IF NOT EXISTS idx_schedules_date ON scheduleservice_schema.schedules USING btree (schedule_date);
CREATE INDEX IF NOT EXISTS idx_schedules_ficha ON scheduleservice_schema.schedules USING btree (ficha_id);
CREATE INDEX IF NOT EXISTS idx_schedules_instructor ON scheduleservice_schema.schedules USING btree (instructor_id);

-- Índices compuestos para paginación eficiente
CREATE INDEX IF NOT EXISTS idx_schedules_ficha_date ON scheduleservice_schema.schedules USING btree (ficha_id, schedule_date);
CREATE INDEX IF NOT EXISTS idx_schedules_date_time ON scheduleservice_schema.schedules USING btree (schedule_date, start_time);

-- Índices para academic_programs
CREATE INDEX IF NOT EXISTS idx_academic_programs_code ON scheduleservice_schema.academic_programs USING btree (program_code);
CREATE INDEX IF NOT EXISTS idx_academic_programs_active ON scheduleservice_schema.academic_programs USING btree (is_active);

-- Índices para academic_groups (fichas)
CREATE INDEX IF NOT EXISTS idx_academic_groups_program ON scheduleservice_schema.academic_groups USING btree (program_id);
CREATE INDEX IF NOT EXISTS idx_academic_groups_code ON scheduleservice_schema.academic_groups USING btree (group_code);

-- Índices para venues (ambientes)
CREATE INDEX IF NOT EXISTS idx_venues_campus ON scheduleservice_schema.venues USING btree (campus_id);
CREATE INDEX IF NOT EXISTS idx_venues_available ON scheduleservice_schema.venues USING btree (is_available);

-- Índices para campuses
CREATE INDEX IF NOT EXISTS idx_campuses_active ON scheduleservice_schema.campuses USING btree (is_active);
