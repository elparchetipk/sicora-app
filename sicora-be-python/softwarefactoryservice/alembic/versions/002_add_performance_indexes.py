"""Add performance indexes for SoftwareFactoryService

Revision ID: 002_add_performance_indexes
Revises: 001_initial_tables
Create Date: 2025-06-29 23:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_performance_indexes'
down_revision = '001_initial_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add performance indexes for SoftwareFactoryService queries"""
    
    # ==========================================
    # FACTORY_PROJECTS INDEXES
    # ==========================================
    
    # Primary search patterns from repositories
    op.create_index(
        'idx_factory_projects_created_by', 
        'factory_projects', 
        ['created_by'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_projects_status', 
        'factory_projects', 
        ['status'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_projects_client_name', 
        'factory_projects', 
        ['client_name'],
        postgresql_using='btree'
    )
    
    # Date range queries for active projects
    op.create_index(
        'idx_factory_projects_date_range', 
        'factory_projects', 
        ['start_date', 'end_date'],
        postgresql_using='btree'
    )
    
    # Status + date composite for performance
    op.create_index(
        'idx_factory_projects_status_dates', 
        'factory_projects', 
        ['status', 'start_date', 'end_date'],
        postgresql_using='btree'
    )
    
    # GIN index for tech_stack array searches
    op.create_index(
        'idx_factory_projects_tech_stack_gin', 
        'factory_projects', 
        ['tech_stack'],
        postgresql_using='gin'
    )
    
    # Full-text search index for name and description
    op.execute("""
        CREATE INDEX idx_factory_projects_fulltext 
        ON factory_projects 
        USING gin(to_tsvector('english', name || ' ' || description))
    """)
    
    # ==========================================
    # FACTORY_TEAMS INDEXES
    # ==========================================
    
    op.create_index(
        'idx_factory_teams_project_id', 
        'factory_teams', 
        ['project_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_teams_tech_lead', 
        'factory_teams', 
        ['tech_lead_instructor_id'],
        postgresql_using='btree'
    )
    
    # Full-text search for team names
    op.execute("""
        CREATE INDEX idx_factory_teams_name_fulltext 
        ON factory_teams 
        USING gin(to_tsvector('english', name))
    """)
    
    # ==========================================
    # FACTORY_TEAM_MEMBERS INDEXES
    # ==========================================
    
    op.create_index(
        'idx_factory_team_members_team_id', 
        'factory_team_members', 
        ['team_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_team_members_apprentice_id', 
        'factory_team_members', 
        ['apprentice_id'],
        postgresql_using='btree'
    )
    
    # Active members query optimization
    op.create_index(
        'idx_factory_team_members_active', 
        'factory_team_members', 
        ['team_id', 'is_active'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_team_members_user_active', 
        'factory_team_members', 
        ['apprentice_id', 'is_active'],
        postgresql_using='btree'
    )
    
    # ==========================================
    # FACTORY_SPRINTS INDEXES
    # ==========================================
    
    op.create_index(
        'idx_factory_sprints_project_id', 
        'factory_sprints', 
        ['project_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_sprints_status', 
        'factory_sprints', 
        ['status'],
        postgresql_using='btree'
    )
    
    # Current sprint query optimization
    op.create_index(
        'idx_factory_sprints_project_status', 
        'factory_sprints', 
        ['project_id', 'status'],
        postgresql_using='btree'
    )
    
    # Date range queries for sprint scheduling
    op.create_index(
        'idx_factory_sprints_date_range', 
        'factory_sprints', 
        ['start_date', 'end_date'],
        postgresql_using='btree'
    )
    
    # Full-text search for sprint name and goal
    op.execute("""
        CREATE INDEX idx_factory_sprints_fulltext 
        ON factory_sprints 
        USING gin(to_tsvector('english', name || ' ' || COALESCE(goal, '')))
    """)
    
    # ==========================================
    # FACTORY_USER_STORIES INDEXES
    # ==========================================
    
    op.create_index(
        'idx_factory_user_stories_project_id', 
        'factory_user_stories', 
        ['project_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_user_stories_sprint_id', 
        'factory_user_stories', 
        ['sprint_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_user_stories_assigned_to', 
        'factory_user_stories', 
        ['assigned_to'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_user_stories_status', 
        'factory_user_stories', 
        ['status'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_user_stories_priority', 
        'factory_user_stories', 
        ['priority'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_user_stories_story_points', 
        'factory_user_stories', 
        ['story_points'],
        postgresql_using='btree'
    )
    
    # Backlog queries optimization
    op.create_index(
        'idx_factory_user_stories_backlog', 
        'factory_user_stories', 
        ['project_id', 'sprint_id', 'status'],
        postgresql_using='btree'
    )
    
    # Sprint statistics queries
    op.create_index(
        'idx_factory_user_stories_sprint_status', 
        'factory_user_stories', 
        ['sprint_id', 'status'],
        postgresql_using='btree'
    )
    
    # Tags array search optimization
    op.create_index(
        'idx_factory_user_stories_tags_gin', 
        'factory_user_stories', 
        ['tags'],
        postgresql_using='gin'
    )
    
    # Dependencies array search
    op.create_index(
        'idx_factory_user_stories_dependencies_gin', 
        'factory_user_stories', 
        ['dependencies'],
        postgresql_using='gin'
    )
    
    # Full-text search for title and description
    op.execute("""
        CREATE INDEX idx_factory_user_stories_fulltext 
        ON factory_user_stories 
        USING gin(to_tsvector('english', title || ' ' || description))
    """)
    
    # ==========================================
    # FACTORY_EVALUATIONS INDEXES
    # ==========================================
    
    op.create_index(
        'idx_factory_evaluations_apprentice_id', 
        'factory_evaluations', 
        ['apprentice_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_evaluations_evaluator_id', 
        'factory_evaluations', 
        ['evaluator_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_evaluations_project_id', 
        'factory_evaluations', 
        ['project_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_evaluations_sprint_id', 
        'factory_evaluations', 
        ['sprint_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_evaluations_type', 
        'factory_evaluations', 
        ['evaluation_type'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_evaluations_date', 
        'factory_evaluations', 
        ['evaluation_date'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_evaluations_score', 
        'factory_evaluations', 
        ['overall_score'],
        postgresql_using='btree'
    )
    
    # Student evaluation history optimization
    op.create_index(
        'idx_factory_evaluations_student_project', 
        'factory_evaluations', 
        ['apprentice_id', 'project_id'],
        postgresql_using='btree'
    )
    
    # Project evaluation reporting
    op.create_index(
        'idx_factory_evaluations_project_date', 
        'factory_evaluations', 
        ['project_id', 'evaluation_date'],
        postgresql_using='btree'
    )
    
    # Date range queries for reporting
    op.create_index(
        'idx_factory_evaluations_date_range', 
        'factory_evaluations', 
        ['evaluation_date', 'project_id'],
        postgresql_using='btree'
    )
    
    # ==========================================
    # FACTORY_TECHNOLOGIES INDEXES
    # ==========================================
    
    op.create_index(
        'idx_factory_technologies_name', 
        'factory_technologies', 
        ['name'],
        postgresql_using='btree',
        unique=True
    )
    
    op.create_index(
        'idx_factory_technologies_category', 
        'factory_technologies', 
        ['category'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_technologies_level', 
        'factory_technologies', 
        ['level'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_technologies_status', 
        'factory_technologies', 
        ['status'],
        postgresql_using='btree'
    )
    
    # Catalog filtering optimization
    op.create_index(
        'idx_factory_technologies_catalog', 
        'factory_technologies', 
        ['category', 'level', 'status'],
        postgresql_using='btree'
    )
    
    # Full-text search for technology name and description
    op.execute("""
        CREATE INDEX idx_factory_technologies_fulltext 
        ON factory_technologies 
        USING gin(to_tsvector('english', name || ' ' || description))
    """)
    
    # ==========================================
    # FACTORY_IMPROVEMENT_PLANS INDEXES
    # ==========================================
    
    op.create_index(
        'idx_factory_improvement_plans_evaluation_id', 
        'factory_improvement_plans', 
        ['evaluation_id'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_improvement_plans_status', 
        'factory_improvement_plans', 
        ['status'],
        postgresql_using='btree'
    )
    
    op.create_index(
        'idx_factory_improvement_plans_competency', 
        'factory_improvement_plans', 
        ['competency_area'],
        postgresql_using='btree'
    )
    
    # ==========================================
    # PAGINATION AND PERFORMANCE OPTIMIZATION
    # ==========================================
    
    # Composite indexes for common paginated queries
    
    # Projects ordered by creation date (most common pagination)
    op.create_index(
        'idx_factory_projects_pagination', 
        'factory_projects', 
        ['created_at', 'id'],
        postgresql_using='btree'
    )
    
    # User stories ordered by priority and creation
    op.create_index(
        'idx_factory_user_stories_pagination', 
        'factory_user_stories', 
        ['priority', 'created_at', 'id'],
        postgresql_using='btree'
    )
    
    # Evaluations ordered by date
    op.create_index(
        'idx_factory_evaluations_pagination', 
        'factory_evaluations', 
        ['evaluation_date', 'id'],
        postgresql_using='btree'
    )
    
    # ==========================================
    # ANALYTICS AND REPORTING INDEXES
    # ==========================================
    
    # Project performance analytics
    op.create_index(
        'idx_factory_projects_analytics', 
        'factory_projects', 
        ['status', 'complexity_level', 'estimated_duration_weeks'],
        postgresql_using='btree'
    )
    
    # Student performance analytics
    op.create_index(
        'idx_factory_evaluations_analytics', 
        'factory_evaluations', 
        ['apprentice_id', 'evaluation_type', 'overall_score'],
        postgresql_using='btree'
    )
    
    # Sprint velocity analytics
    op.create_index(
        'idx_factory_sprints_analytics', 
        'factory_sprints', 
        ['project_id', 'status', 'start_date'],
        postgresql_using='btree'
    )


def downgrade() -> None:
    """Remove performance indexes for SoftwareFactoryService"""
    
    # Remove all created indexes
    indexes_to_drop = [
        # Projects
        'idx_factory_projects_created_by',
        'idx_factory_projects_status',
        'idx_factory_projects_client_name',
        'idx_factory_projects_date_range',
        'idx_factory_projects_status_dates',
        'idx_factory_projects_tech_stack_gin',
        'idx_factory_projects_fulltext',
        'idx_factory_projects_pagination',
        'idx_factory_projects_analytics',
        
        # Teams
        'idx_factory_teams_project_id',
        'idx_factory_teams_tech_lead',
        'idx_factory_teams_name_fulltext',
        
        # Team Members
        'idx_factory_team_members_team_id',
        'idx_factory_team_members_apprentice_id',
        'idx_factory_team_members_active',
        'idx_factory_team_members_user_active',
        
        # Sprints
        'idx_factory_sprints_project_id',
        'idx_factory_sprints_status',
        'idx_factory_sprints_project_status',
        'idx_factory_sprints_date_range',
        'idx_factory_sprints_fulltext',
        'idx_factory_sprints_analytics',
        
        # User Stories
        'idx_factory_user_stories_project_id',
        'idx_factory_user_stories_sprint_id',
        'idx_factory_user_stories_assigned_to',
        'idx_factory_user_stories_status',
        'idx_factory_user_stories_priority',
        'idx_factory_user_stories_story_points',
        'idx_factory_user_stories_backlog',
        'idx_factory_user_stories_sprint_status',
        'idx_factory_user_stories_tags_gin',
        'idx_factory_user_stories_dependencies_gin',
        'idx_factory_user_stories_fulltext',
        'idx_factory_user_stories_pagination',
        
        # Evaluations
        'idx_factory_evaluations_apprentice_id',
        'idx_factory_evaluations_evaluator_id',
        'idx_factory_evaluations_project_id',
        'idx_factory_evaluations_sprint_id',
        'idx_factory_evaluations_type',
        'idx_factory_evaluations_date',
        'idx_factory_evaluations_score',
        'idx_factory_evaluations_student_project',
        'idx_factory_evaluations_project_date',
        'idx_factory_evaluations_date_range',
        'idx_factory_evaluations_pagination',
        'idx_factory_evaluations_analytics',
        
        # Technologies
        'idx_factory_technologies_name',
        'idx_factory_technologies_category',
        'idx_factory_technologies_level',
        'idx_factory_technologies_status',
        'idx_factory_technologies_catalog',
        'idx_factory_technologies_fulltext',
        
        # Improvement Plans
        'idx_factory_improvement_plans_evaluation_id',
        'idx_factory_improvement_plans_status',
        'idx_factory_improvement_plans_competency',
    ]
    
    for index_name in indexes_to_drop:
        op.drop_index(index_name, table_name=None)
