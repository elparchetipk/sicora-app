"""Add advanced analytics and query optimization

Revision ID: 003_analytics_optimization
Revises: 002_add_performance_indexes
Create Date: 2025-06-29 23:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_analytics_optimization'
down_revision = '002_add_performance_indexes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add advanced analytics optimization for SoftwareFactoryService"""
    
    # ==========================================
    # MATERIALIZED VIEWS FOR PERFORMANCE
    # ==========================================
    
    # Project Statistics View
    op.execute("""
        CREATE MATERIALIZED VIEW mv_project_statistics AS
        WITH project_stats AS (
            SELECT 
                p.id as project_id,
                p.name as project_name,
                p.status,
                p.complexity_level,
                p.estimated_duration_weeks,
                p.start_date,
                p.end_date,
                COUNT(DISTINCT t.id) as total_teams,
                COUNT(DISTINCT tm.apprentice_id) as total_apprentices,
                COUNT(DISTINCT s.id) as total_sprints,
                COUNT(DISTINCT us.id) as total_user_stories,
                COUNT(DISTINCT CASE WHEN us.status = 'done' THEN us.id END) as completed_stories,
                SUM(CASE WHEN us.status = 'done' THEN us.story_points ELSE 0 END) as completed_points,
                SUM(us.story_points) as total_points,
                AVG(e.overall_score) as avg_evaluation_score,
                COUNT(DISTINCT e.id) as total_evaluations,
                EXTRACT(DAYS FROM COALESCE(p.end_date, CURRENT_DATE) - p.start_date) as actual_duration_days
            FROM factory_projects p
            LEFT JOIN factory_teams t ON p.id = t.project_id
            LEFT JOIN factory_team_members tm ON t.id = tm.team_id AND tm.is_active = true
            LEFT JOIN factory_sprints s ON p.id = s.project_id
            LEFT JOIN factory_user_stories us ON p.id = us.project_id
            LEFT JOIN factory_evaluations e ON p.id = e.project_id
            GROUP BY p.id, p.name, p.status, p.complexity_level, p.estimated_duration_weeks, p.start_date, p.end_date
        )
        SELECT 
            *,
            CASE 
                WHEN total_points > 0 THEN (completed_points::float / total_points * 100)
                ELSE 0 
            END as completion_percentage,
            CASE 
                WHEN total_user_stories > 0 THEN (completed_stories::float / total_user_stories * 100)
                ELSE 0 
            END as story_completion_percentage
        FROM project_stats;
    """)
    
    # Create index on the materialized view
    op.create_index(
        'idx_mv_project_statistics_project_id',
        'mv_project_statistics',
        ['project_id'],
        postgresql_using='btree',
        unique=True
    )
    
    op.create_index(
        'idx_mv_project_statistics_status',
        'mv_project_statistics',
        ['status'],
        postgresql_using='btree'
    )
    
    # Student Performance View
    op.execute("""
        CREATE MATERIALIZED VIEW mv_student_performance AS
        WITH student_stats AS (
            SELECT 
                e.apprentice_id,
                p.id as project_id,
                p.name as project_name,
                COUNT(DISTINCT e.id) as total_evaluations,
                AVG(e.overall_score) as avg_overall_score,
                AVG(e.tech_coding_quality) as avg_coding_quality,
                AVG(e.tech_problem_solving) as avg_problem_solving,
                AVG(e.tech_technology_adoption) as avg_technology_adoption,
                AVG(e.tech_testing_practices) as avg_testing_practices,
                AVG(e.soft_communication) as avg_communication,
                AVG(e.soft_teamwork) as avg_teamwork,
                AVG(e.soft_leadership) as avg_leadership,
                AVG(e.soft_adaptability) as avg_adaptability,
                COUNT(DISTINCT us.id) as assigned_stories,
                COUNT(DISTINCT CASE WHEN us.status = 'done' THEN us.id END) as completed_stories,
                SUM(CASE WHEN us.status = 'done' THEN us.story_points ELSE 0 END) as completed_points,
                SUM(us.story_points) as total_assigned_points,
                MIN(e.evaluation_date) as first_evaluation,
                MAX(e.evaluation_date) as last_evaluation
            FROM factory_evaluations e
            JOIN factory_projects p ON e.project_id = p.id
            LEFT JOIN factory_user_stories us ON e.apprentice_id = us.assigned_to AND e.project_id = us.project_id
            GROUP BY e.apprentice_id, p.id, p.name
        )
        SELECT 
            *,
            CASE 
                WHEN total_assigned_points > 0 THEN (completed_points::float / total_assigned_points * 100)
                ELSE 0 
            END as velocity_percentage,
            CASE 
                WHEN assigned_stories > 0 THEN (completed_stories::float / assigned_stories * 100)
                ELSE 0 
            END as story_completion_rate
        FROM student_stats;
    """)
    
    # Create indexes on student performance view
    op.create_index(
        'idx_mv_student_performance_apprentice',
        'mv_student_performance',
        ['apprentice_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_mv_student_performance_project',
        'mv_student_performance',
        ['project_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_mv_student_performance_score',
        'mv_student_performance',
        ['avg_overall_score'],
        postgresql_using='btree'
    )
    
    # Technology Usage Statistics View
    op.execute("""
        CREATE MATERIALIZED VIEW mv_technology_usage AS
        SELECT 
            t.id as technology_id,
            t.name as technology_name,
            t.category,
            t.level,
            COUNT(DISTINCT p.id) as projects_using,
            COUNT(DISTINCT tm.apprentice_id) as apprentices_exposed,
            AVG(ps.completion_percentage) as avg_project_success_rate,
            COUNT(DISTINCT CASE WHEN p.status = 'completed' THEN p.id END) as completed_projects,
            COUNT(DISTINCT CASE WHEN p.status = 'active' THEN p.id END) as active_projects
        FROM factory_technologies t
        LEFT JOIN factory_projects p ON t.name = ANY(p.tech_stack)
        LEFT JOIN factory_teams te ON p.id = te.project_id
        LEFT JOIN factory_team_members tm ON te.id = tm.team_id AND tm.is_active = true
        LEFT JOIN mv_project_statistics ps ON p.id = ps.project_id
        WHERE t.status = 'active'
        GROUP BY t.id, t.name, t.category, t.level;
    """)
    
    # Create indexes on technology usage view
    op.create_index(
        'idx_mv_technology_usage_tech_id',
        'mv_technology_usage',
        ['technology_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_mv_technology_usage_category',
        'mv_technology_usage',
        ['category'],
        postgresql_using='btree'
    )
    
    # ==========================================
    # SPECIALIZED INDEXES FOR COMPLEX QUERIES
    # ==========================================
    
    # Partial indexes for active data (reduce index size)
    op.create_index(
        'idx_factory_projects_active_only',
        'factory_projects',
        ['id', 'name', 'created_at'],
        postgresql_where="status IN ('planning', 'active')",
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_sprints_active_only',
        'factory_sprints',
        ['project_id', 'start_date', 'end_date'],
        postgresql_where="status = 'active'",
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_user_stories_in_progress',
        'factory_user_stories',
        ['assigned_to', 'project_id', 'priority'],
        postgresql_where="status IN ('todo', 'in_progress', 'review')",
        postgresql_using='btree'
    )
    
    # Expression indexes for calculated fields
    op.execute("""
        CREATE INDEX idx_factory_evaluations_score_category
        ON factory_evaluations 
        USING btree (
            CASE 
                WHEN overall_score >= 4.5 THEN 'excellent'
                WHEN overall_score >= 3.5 THEN 'good'
                WHEN overall_score >= 2.5 THEN 'average'
                ELSE 'needs_improvement'
            END
        )
    """)
    
    # Multi-column statistics for better query planning
    op.execute("""
        CREATE STATISTICS stats_projects_tech_complexity 
        ON status, tech_stack, complexity_level 
        FROM factory_projects
    """)
    
    op.execute("""
        CREATE STATISTICS stats_evaluations_scores 
        ON apprentice_id, evaluation_type, overall_score, evaluation_date 
        FROM factory_evaluations
    """)
    
    op.execute("""
        CREATE STATISTICS stats_user_stories_workflow 
        ON project_id, sprint_id, status, priority, story_points 
        FROM factory_user_stories
    """)
    
    # ==========================================
    # FUNCTIONS FOR REFRESH MATERIALIZED VIEWS
    # ==========================================
    
    op.execute("""
        CREATE OR REPLACE FUNCTION refresh_softwarefactory_analytics()
        RETURNS void AS $$
        BEGIN
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_project_statistics;
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_student_performance;
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_technology_usage;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Create a stored procedure for pagination optimization
    op.execute("""
        CREATE OR REPLACE FUNCTION get_paginated_projects(
            p_limit INTEGER DEFAULT 20,
            p_offset INTEGER DEFAULT 0,
            p_status VARCHAR DEFAULT NULL,
            p_instructor_id UUID DEFAULT NULL,
            p_search_term VARCHAR DEFAULT NULL
        ) RETURNS TABLE (
            id UUID,
            name VARCHAR,
            description TEXT,
            status VARCHAR,
            complexity_level VARCHAR,
            created_at TIMESTAMP,
            total_count BIGINT
        ) AS $$
        DECLARE
            base_query TEXT;
            count_query TEXT;
            where_clause TEXT := '';
            total_records BIGINT;
        BEGIN
            -- Build WHERE clause dynamically
            IF p_status IS NOT NULL THEN
                where_clause := where_clause || format(' AND status = %L', p_status);
            END IF;
            
            IF p_instructor_id IS NOT NULL THEN
                where_clause := where_clause || format(' AND created_by = %L', p_instructor_id);
            END IF;
            
            IF p_search_term IS NOT NULL THEN
                where_clause := where_clause || format(' AND (name ILIKE %L OR description ILIKE %L)', 
                    '%' || p_search_term || '%', '%' || p_search_term || '%');
            END IF;
            
            -- Remove leading AND
            IF where_clause != '' THEN
                where_clause := 'WHERE ' || substring(where_clause from 6);
            END IF;
            
            -- Get total count
            count_query := format('SELECT COUNT(*) FROM factory_projects %s', where_clause);
            EXECUTE count_query INTO total_records;
            
            -- Build and execute main query
            base_query := format('
                SELECT fp.id, fp.name, fp.description, fp.status, fp.complexity_level, fp.created_at, %L::BIGINT
                FROM factory_projects fp
                %s
                ORDER BY fp.created_at DESC, fp.id
                LIMIT %L OFFSET %L
            ', total_records, where_clause, p_limit, p_offset);
            
            RETURN QUERY EXECUTE base_query;
        END;
        $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    """Remove advanced analytics optimization"""
    
    # Drop functions
    op.execute("DROP FUNCTION IF EXISTS refresh_softwarefactory_analytics()")
    op.execute("DROP FUNCTION IF EXISTS get_paginated_projects(INTEGER, INTEGER, VARCHAR, UUID, VARCHAR)")
    
    # Drop statistics
    op.execute("DROP STATISTICS IF EXISTS stats_projects_tech_complexity")
    op.execute("DROP STATISTICS IF EXISTS stats_evaluations_scores")
    op.execute("DROP STATISTICS IF EXISTS stats_user_stories_workflow")
    
    # Drop expression indexes
    op.drop_index('idx_factory_evaluations_score_category')
    
    # Drop partial indexes
    op.drop_index('idx_factory_projects_active_only')
    op.drop_index('idx_factory_sprints_active_only')
    op.drop_index('idx_factory_user_stories_in_progress')
    
    # Drop materialized view indexes
    op.drop_index('idx_mv_project_statistics_project_id')
    op.drop_index('idx_mv_project_statistics_status')
    op.drop_index('idx_mv_student_performance_apprentice')
    op.drop_index('idx_mv_student_performance_project')
    op.drop_index('idx_mv_student_performance_score')
    op.drop_index('idx_mv_technology_usage_tech_id')
    op.drop_index('idx_mv_technology_usage_category')
    
    # Drop materialized views
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_technology_usage")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_student_performance")  
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_project_statistics")
