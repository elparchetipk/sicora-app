-- Migration: Create MEvalService Schema and Tables
-- Version: 001
-- Date: 2025-06-29

-- Create schema
CREATE SCHEMA IF NOT EXISTS mevalservice_schema;

-- Create UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create committees table
CREATE TABLE IF NOT EXISTS mevalservice_schema.committees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    committee_date TIMESTAMP NOT NULL,
    committee_type VARCHAR(50) NOT NULL CHECK (committee_type IN ('MONTHLY', 'EXTRAORDINARY', 'APPEALS', 'SPECIAL')),
    status VARCHAR(50) NOT NULL DEFAULT 'SCHEDULED' CHECK (status IN ('SCHEDULED', 'IN_SESSION', 'COMPLETED', 'CANCELLED', 'POSTPONED')),
    program_id UUID,
    academic_period VARCHAR(20),
    agenda_generated BOOLEAN DEFAULT FALSE,
    quorum_achieved BOOLEAN DEFAULT FALSE,
    session_minutes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create committee_members table
CREATE TABLE IF NOT EXISTS mevalservice_schema.committee_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    committee_id UUID NOT NULL REFERENCES mevalservice_schema.committees(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('PRESIDENT', 'SECRETARY', 'INSTRUCTOR', 'COORDINATOR', 'STUDENT_REP')),
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE')),
    appointment_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create student_cases table
CREATE TABLE IF NOT EXISTS mevalservice_schema.student_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL,
    committee_id UUID NOT NULL REFERENCES mevalservice_schema.committees(id),
    case_type VARCHAR(50) NOT NULL CHECK (case_type IN ('RECOGNITION', 'IMPROVEMENT_PLAN', 'SANCTION', 'APPEAL', 'FOLLOW_UP')),
    case_status VARCHAR(50) NOT NULL DEFAULT 'DETECTED' CHECK (case_status IN ('DETECTED', 'PENDING', 'IN_REVIEW', 'RESOLVED')),
    automatic_detection BOOLEAN DEFAULT TRUE,
    detection_criteria JSONB,
    case_description TEXT,
    evidence_documents JSONB,
    instructor_comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create improvement_plans table  
CREATE TABLE IF NOT EXISTS mevalservice_schema.improvement_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_case_id UUID NOT NULL REFERENCES mevalservice_schema.student_cases(id) ON DELETE CASCADE,
    student_id UUID NOT NULL,
    instructor_id UUID NOT NULL,
    plan_title VARCHAR(200) NOT NULL,
    plan_description TEXT NOT NULL,
    objectives TEXT NOT NULL,
    activities JSONB,
    expected_results TEXT,
    evaluation_criteria TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    instructor_feedback TEXT,
    student_feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sanctions table
CREATE TABLE IF NOT EXISTS mevalservice_schema.sanctions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_case_id UUID NOT NULL REFERENCES mevalservice_schema.student_cases(id) ON DELETE CASCADE,
    student_id UUID NOT NULL,
    sanction_type VARCHAR(100) NOT NULL CHECK (sanction_type IN ('LLAMADO_ATENCION', 'CONDICIONAMIENTO_MATRICULA', 'CANCELACION_MATRICULA')),
    sanction_description TEXT NOT NULL,
    justification TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL CHECK (severity IN ('LEVE', 'GRAVE', 'GRAVISIMA')),
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'ACTIVE', 'COMPLETED', 'REVOKED', 'APPEALED')),
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_appealable BOOLEAN DEFAULT TRUE,
    appeal_deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create appeals table
CREATE TABLE IF NOT EXISTS mevalservice_schema.appeals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_case_id UUID NOT NULL REFERENCES mevalservice_schema.student_cases(id),
    student_id UUID NOT NULL,
    appeal_type VARCHAR(50) NOT NULL CHECK (appeal_type IN ('SANCTION_APPEAL', 'DECISION_APPEAL', 'PROCESS_APPEAL')),
    appeal_subject VARCHAR(200) NOT NULL,
    appeal_description TEXT NOT NULL,
    justification TEXT NOT NULL,
    evidence_documents JSONB,
    requested_resolution TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'SUBMITTED' CHECK (status IN ('SUBMITTED', 'UNDER_REVIEW', 'ACCEPTED', 'REJECTED', 'WITHDRAWN')),
    submission_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    review_date TIMESTAMP,
    resolution_date TIMESTAMP,
    reviewer_id UUID,
    reviewer_notes TEXT,
    final_resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create committee_decisions table
CREATE TABLE IF NOT EXISTS mevalservice_schema.committee_decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    committee_id UUID NOT NULL REFERENCES mevalservice_schema.committees(id),
    student_case_id UUID REFERENCES mevalservice_schema.student_cases(id),
    decision_number VARCHAR(50) UNIQUE NOT NULL,
    decision_type VARCHAR(100) NOT NULL CHECK (decision_type IN ('CASE_RESOLUTION', 'SANCTION_APPROVAL', 'APPEAL_RESOLUTION', 'POLICY_DECISION', 'RECOGNITION')),
    decision_title VARCHAR(200) NOT NULL,
    decision_description TEXT NOT NULL,
    resolution TEXT NOT NULL,
    justification TEXT NOT NULL,
    voting_result JSONB,
    attendees_list JSONB,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'APPROVED', 'EXECUTED', 'APPEALED')),
    decision_date TIMESTAMP NOT NULL,
    execution_date TIMESTAMP,
    president_signature BOOLEAN DEFAULT FALSE,
    secretary_signature BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_committees_date ON mevalservice_schema.committees(committee_date);
CREATE INDEX IF NOT EXISTS idx_committees_type ON mevalservice_schema.committees(committee_type);
CREATE INDEX IF NOT EXISTS idx_committees_status ON mevalservice_schema.committees(status);

CREATE INDEX IF NOT EXISTS idx_committee_members_committee_id ON mevalservice_schema.committee_members(committee_id);
CREATE INDEX IF NOT EXISTS idx_committee_members_user_id ON mevalservice_schema.committee_members(user_id);

CREATE INDEX IF NOT EXISTS idx_student_cases_student_id ON mevalservice_schema.student_cases(student_id);
CREATE INDEX IF NOT EXISTS idx_student_cases_committee_id ON mevalservice_schema.student_cases(committee_id);
CREATE INDEX IF NOT EXISTS idx_student_cases_type ON mevalservice_schema.student_cases(case_type);
CREATE INDEX IF NOT EXISTS idx_student_cases_status ON mevalservice_schema.student_cases(case_status);

CREATE INDEX IF NOT EXISTS idx_improvement_plans_student_case_id ON mevalservice_schema.improvement_plans(student_case_id);
CREATE INDEX IF NOT EXISTS idx_improvement_plans_student_id ON mevalservice_schema.improvement_plans(student_id);
CREATE INDEX IF NOT EXISTS idx_improvement_plans_status ON mevalservice_schema.improvement_plans(status);

CREATE INDEX IF NOT EXISTS idx_sanctions_student_case_id ON mevalservice_schema.sanctions(student_case_id);
CREATE INDEX IF NOT EXISTS idx_sanctions_student_id ON mevalservice_schema.sanctions(student_id);
CREATE INDEX IF NOT EXISTS idx_sanctions_status ON mevalservice_schema.sanctions(status);

CREATE INDEX IF NOT EXISTS idx_appeals_student_case_id ON mevalservice_schema.appeals(student_case_id);
CREATE INDEX IF NOT EXISTS idx_appeals_student_id ON mevalservice_schema.appeals(student_id);
CREATE INDEX IF NOT EXISTS idx_appeals_status ON mevalservice_schema.appeals(status);

CREATE INDEX IF NOT EXISTS idx_committee_decisions_committee_id ON mevalservice_schema.committee_decisions(committee_id);
CREATE INDEX IF NOT EXISTS idx_committee_decisions_student_case_id ON mevalservice_schema.committee_decisions(student_case_id);
CREATE INDEX IF NOT EXISTS idx_committee_decisions_type ON mevalservice_schema.committee_decisions(decision_type);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION mevalservice_schema.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_committees_updated_at BEFORE UPDATE ON mevalservice_schema.committees FOR EACH ROW EXECUTE FUNCTION mevalservice_schema.update_updated_at_column();
CREATE TRIGGER update_committee_members_updated_at BEFORE UPDATE ON mevalservice_schema.committee_members FOR EACH ROW EXECUTE FUNCTION mevalservice_schema.update_updated_at_column();
CREATE TRIGGER update_student_cases_updated_at BEFORE UPDATE ON mevalservice_schema.student_cases FOR EACH ROW EXECUTE FUNCTION mevalservice_schema.update_updated_at_column();
CREATE TRIGGER update_improvement_plans_updated_at BEFORE UPDATE ON mevalservice_schema.improvement_plans FOR EACH ROW EXECUTE FUNCTION mevalservice_schema.update_updated_at_column();
CREATE TRIGGER update_sanctions_updated_at BEFORE UPDATE ON mevalservice_schema.sanctions FOR EACH ROW EXECUTE FUNCTION mevalservice_schema.update_updated_at_column();
CREATE TRIGGER update_appeals_updated_at BEFORE UPDATE ON mevalservice_schema.appeals FOR EACH ROW EXECUTE FUNCTION mevalservice_schema.update_updated_at_column();
CREATE TRIGGER update_committee_decisions_updated_at BEFORE UPDATE ON mevalservice_schema.committee_decisions FOR EACH ROW EXECUTE FUNCTION mevalservice_schema.update_updated_at_column();
