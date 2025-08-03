-- Crear tablas para EvalinService en OneVision
-- Base: migración evalin_001_initial.py

-- Usar el esquema evalinservice_schema
SET search_path TO evalinservice_schema;

-- Crear ENUMs
CREATE TYPE evalinservice_schema.questiontype AS ENUM ('SCALE_1_5', 'TEXT', 'MULTIPLE_CHOICE');
CREATE TYPE evalinservice_schema.periodstatus AS ENUM ('SCHEDULED', 'ACTIVE', 'COMPLETED', 'CANCELLED');
CREATE TYPE evalinservice_schema.evaluationstatus AS ENUM ('DRAFT', 'SUBMITTED');

-- Questions table
CREATE TABLE evalinservice_schema.questions (
    id UUID PRIMARY KEY,
    text VARCHAR(500) NOT NULL,
    type evalinservice_schema.questiontype NOT NULL,
    options JSON,
    is_required BOOLEAN NOT NULL DEFAULT TRUE,
    "order" INTEGER,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT min_text_length CHECK (length(text) >= 10),
    CONSTRAINT max_text_length CHECK (length(text) <= 500)
);

-- Índices para questions
CREATE INDEX ix_questions_type ON evalinservice_schema.questions(type);
CREATE INDEX ix_questions_is_required ON evalinservice_schema.questions(is_required);

-- Questionnaires table
CREATE TABLE evalinservice_schema.questionnaires (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT min_name_length CHECK (length(name) >= 5),
    CONSTRAINT max_name_length CHECK (length(name) <= 200)
);

-- Índices para questionnaires
CREATE INDEX ix_questionnaires_name ON evalinservice_schema.questionnaires(name);
CREATE INDEX ix_questionnaires_is_active ON evalinservice_schema.questionnaires(is_active);

-- Questionnaire Questions association table
CREATE TABLE evalinservice_schema.questionnaire_questions (
    questionnaire_id UUID NOT NULL,
    question_id UUID NOT NULL,
    "order" INTEGER NOT NULL,
    PRIMARY KEY (questionnaire_id, question_id),
    FOREIGN KEY (question_id) REFERENCES evalinservice_schema.questions(id) ON DELETE CASCADE,
    FOREIGN KEY (questionnaire_id) REFERENCES evalinservice_schema.questionnaires(id) ON DELETE CASCADE,
    CONSTRAINT unique_question_order_per_questionnaire UNIQUE (questionnaire_id, "order")
);

-- Evaluation Periods table
CREATE TABLE evalinservice_schema.evaluation_periods (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    questionnaire_id UUID NOT NULL,
    status evalinservice_schema.periodstatus NOT NULL DEFAULT 'SCHEDULED',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (questionnaire_id) REFERENCES evalinservice_schema.questionnaires(id),
    CONSTRAINT valid_date_range CHECK (end_date > start_date),
    CONSTRAINT min_period_name_length CHECK (length(name) >= 5),
    CONSTRAINT max_period_name_length CHECK (length(name) <= 200)
);

-- Índices para evaluation_periods
CREATE INDEX ix_evaluation_periods_name ON evalinservice_schema.evaluation_periods(name);
CREATE INDEX ix_evaluation_periods_status ON evalinservice_schema.evaluation_periods(status);
CREATE INDEX ix_evaluation_periods_start_date ON evalinservice_schema.evaluation_periods(start_date);
CREATE INDEX ix_evaluation_periods_end_date ON evalinservice_schema.evaluation_periods(end_date);

-- Evaluations table
CREATE TABLE evalinservice_schema.evaluations (
    id UUID PRIMARY KEY,
    student_id UUID NOT NULL,
    instructor_id UUID NOT NULL,
    period_id UUID NOT NULL,
    responses JSON NOT NULL,
    comments TEXT,
    status evalinservice_schema.evaluationstatus NOT NULL DEFAULT 'DRAFT',
    submitted_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (period_id) REFERENCES evalinservice_schema.evaluation_periods(id),
    CONSTRAINT unique_student_instructor_period UNIQUE (student_id, instructor_id, period_id),
    CONSTRAINT submitted_status_consistency CHECK (
        (status = 'SUBMITTED' AND submitted_at IS NOT NULL) OR (status = 'DRAFT')
    )
);

-- Índices para evaluations
CREATE INDEX ix_evaluations_student_id ON evalinservice_schema.evaluations(student_id);
CREATE INDEX ix_evaluations_instructor_id ON evalinservice_schema.evaluations(instructor_id);
CREATE INDEX ix_evaluations_status ON evalinservice_schema.evaluations(status);
CREATE INDEX ix_evaluations_submitted_at ON evalinservice_schema.evaluations(submitted_at);

-- Verificar la creación
SELECT 'Tablas creadas exitosamente para EvalinService' as resultado;
