-- Migration: 001_initial_setup.sql
-- Description: Initial database setup for KbService

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create custom types
DO $$ BEGIN
    CREATE TYPE document_status AS ENUM ('draft', 'review', 'approved', 'published', 'archived');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE document_category AS ENUM ('tutorial', 'api_doc', 'troubleshooting', 'best_practice', 'faq', 'announcement', 'policy', 'guide');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE audience_type AS ENUM ('student', 'teacher', 'admin', 'developer', 'all');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE faq_status AS ENUM ('draft', 'review', 'approved', 'published', 'archived');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE faq_priority AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_documents_tenant_status ON documents(tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_documents_category_audience ON documents(category, audience);
CREATE INDEX IF NOT EXISTS idx_documents_published_at ON documents(published_at) WHERE status = 'published';
CREATE INDEX IF NOT EXISTS idx_documents_embeddings_cosine ON documents USING ivfflat (content_embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_faqs_tenant_status ON faqs(tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_faqs_category_priority ON faqs(category, priority);
CREATE INDEX IF NOT EXISTS idx_faqs_overall_score ON faqs(overall_score DESC);
CREATE INDEX IF NOT EXISTS idx_faqs_question_embeddings ON faqs USING ivfflat (question_embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_analytics_events_tenant_resource ON analytics_events(tenant_id, resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_timestamp ON analytics_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_search_analytics_tenant_timestamp ON search_analytics(tenant_id, timestamp);

-- Create full-text search configurations
CREATE INDEX IF NOT EXISTS idx_documents_fulltext ON documents USING gin(to_tsvector('english', title || ' ' || content));
CREATE INDEX IF NOT EXISTS idx_faqs_fulltext ON faqs USING gin(to_tsvector('english', question || ' ' || answer));

-- Create functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
DROP TRIGGER IF EXISTS update_documents_updated_at ON documents;
CREATE TRIGGER update_documents_updated_at 
    BEFORE UPDATE ON documents 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_faqs_updated_at ON faqs;
CREATE TRIGGER update_faqs_updated_at 
    BEFORE UPDATE ON faqs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function for search scoring
CREATE OR REPLACE FUNCTION calculate_search_score(
    text_similarity REAL,
    vector_similarity REAL,
    view_count INTEGER,
    rating REAL
) RETURNS REAL AS $$
BEGIN
    RETURN (
        text_similarity * 0.3 +
        vector_similarity * 0.4 +
        LEAST(view_count::REAL / 1000.0, 1.0) * 0.2 +
        rating * 0.1
    );
END;
$$ language 'plpgsql' IMMUTABLE;
