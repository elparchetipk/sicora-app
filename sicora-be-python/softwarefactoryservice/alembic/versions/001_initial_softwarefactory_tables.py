"""Initial softwarefactoryservice tables with pagination optimizations

Revision ID: 001_initial_softwarefactory
Revises: 
Create Date: 2025-06-29 23:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_softwarefactory'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Asegurar que estamos trabajando en el esquema correcto
    op.execute("SET search_path TO softwarefactoryservice_schema")
    
    # ###############################################
    # TABLA: projects
    # ###############################################
    op.create_table('projects',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('instructor_id', sa.String(255), nullable=False),
        sa.Column('course_id', sa.String(255), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('client_info', sa.JSON(), nullable=True),
        sa.Column('tech_stack', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('complexity_level', sa.String(50), nullable=False),
        sa.Column('max_teams', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('max_members_per_team', sa.Integer(), nullable=False, server_default='6'),
        sa.Column('evaluation_criteria', sa.JSON(), nullable=True),
        sa.Column('deliverables', sa.JSON(), nullable=True),
        sa.Column('milestones', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='softwarefactoryservice_schema'
    )
    
    # Índices optimizados para paginación y filtrado
    op.create_index('idx_projects_instructor_created', 'projects', ['instructor_id', 'created_at'], schema='softwarefactoryservice_schema')
    op.create_index('idx_projects_course_status', 'projects', ['course_id', 'status'], schema='softwarefactoryservice_schema')
    op.create_index('idx_projects_status_created', 'projects', ['status', 'created_at'], schema='softwarefactoryservice_schema')
    op.create_index('idx_projects_dates', 'projects', ['start_date', 'end_date'], schema='softwarefactoryservice_schema')
    
    # ###############################################
    # TABLA: technologies
    # ###############################################
    op.create_table('technologies',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('version', sa.String(50), nullable=True),
        sa.Column('documentation_url', sa.String(500), nullable=True),
        sa.Column('license_type', sa.String(100), nullable=True),
        sa.Column('learning_difficulty', sa.String(50), nullable=False),
        sa.Column('is_free', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('learning_resources', sa.JSON(), nullable=True),
        sa.Column('prerequisites', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('use_cases', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='softwarefactoryservice_schema'
    )
    
    # Índices para búsqueda y filtrado eficiente
    op.create_index('idx_technologies_category_name', 'technologies', ['category', 'name'], schema='softwarefactoryservice_schema')
    op.create_index('idx_technologies_difficulty', 'technologies', ['learning_difficulty'], schema='softwarefactoryservice_schema')
    op.create_index('idx_technologies_free', 'technologies', ['is_free'], schema='softwarefactoryservice_schema')
    
    # ###############################################
    # TABLA: teams
    # ###############################################
    op.create_table('teams',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('project_id', sa.String(255), nullable=False),
        sa.Column('leader_id', sa.String(255), nullable=False),
        sa.Column('max_members', sa.Integer(), nullable=False, server_default='6'),
        sa.Column('current_size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('focus_area', sa.String(100), nullable=True),
        sa.Column('methodology', sa.String(100), nullable=False),
        sa.Column('rotation_schedule', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['softwarefactoryservice_schema.projects.id'], ondelete='CASCADE'),
        schema='softwarefactoryservice_schema'
    )
    
    # Índices para queries frecuentes
    op.create_index('idx_teams_project', 'teams', ['project_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_teams_leader', 'teams', ['leader_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_teams_project_created', 'teams', ['project_id', 'created_at'], schema='softwarefactoryservice_schema')
    
    # ###############################################
    # TABLA: team_members
    # ###############################################
    op.create_table('team_members',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('team_id', sa.String(255), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('role', sa.String(100), nullable=False),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('contributions', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['team_id'], ['softwarefactoryservice_schema.teams.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('team_id', 'user_id', name='uq_team_member'),
        schema='softwarefactoryservice_schema'
    )
    
    # Índices para búsquedas de membresía
    op.create_index('idx_team_members_team', 'team_members', ['team_id', 'is_active'], schema='softwarefactoryservice_schema')
    op.create_index('idx_team_members_user', 'team_members', ['user_id', 'is_active'], schema='softwarefactoryservice_schema')
    
    # ###############################################
    # TABLA: sprints
    # ###############################################
    op.create_table('sprints',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('project_id', sa.String(255), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('goal', sa.Text(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('capacity_hours', sa.Integer(), nullable=True),
        sa.Column('completed_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('velocity', sa.Float(), nullable=True),
        sa.Column('retrospective_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['softwarefactoryservice_schema.projects.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('project_id', 'number', name='uq_project_sprint_number'),
        schema='softwarefactoryservice_schema'
    )
    
    # Índices para consultas de sprint
    op.create_index('idx_sprints_project', 'sprints', ['project_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_sprints_status_dates', 'sprints', ['status', 'start_date', 'end_date'], schema='softwarefactoryservice_schema')
    op.create_index('idx_sprints_project_number', 'sprints', ['project_id', 'number'], schema='softwarefactoryservice_schema')
    
    # ###############################################
    # TABLA: user_stories
    # ###############################################
    op.create_table('user_stories',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('project_id', sa.String(255), nullable=False),
        sa.Column('sprint_id', sa.String(255), nullable=True),
        sa.Column('assignee_id', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('story_points', sa.Integer(), nullable=True),
        sa.Column('business_value', sa.Integer(), nullable=True),
        sa.Column('acceptance_criteria', sa.JSON(), nullable=True),
        sa.Column('academic_criteria', sa.JSON(), nullable=True),
        sa.Column('technical_notes', sa.Text(), nullable=True),
        sa.Column('estimated_hours', sa.Integer(), nullable=True),
        sa.Column('actual_hours', sa.Integer(), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['softwarefactoryservice_schema.projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sprint_id'], ['softwarefactoryservice_schema.sprints.id'], ondelete='SET NULL'),
        schema='softwarefactoryservice_schema'
    )
    
    # Índices críticos para paginación y filtrado
    op.create_index('idx_user_stories_project', 'user_stories', ['project_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_user_stories_sprint', 'user_stories', ['sprint_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_user_stories_assignee', 'user_stories', ['assignee_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_user_stories_status_priority', 'user_stories', ['status', 'priority'], schema='softwarefactoryservice_schema')
    op.create_index('idx_user_stories_project_status', 'user_stories', ['project_id', 'status'], schema='softwarefactoryservice_schema')
    op.create_index('idx_user_stories_backlog', 'user_stories', ['project_id'], where="sprint_id IS NULL", schema='softwarefactoryservice_schema')
    
    # ###############################################
    # TABLA: evaluations
    # ###############################################
    op.create_table('evaluations',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('project_id', sa.String(255), nullable=False),
        sa.Column('sprint_id', sa.String(255), nullable=True),
        sa.Column('student_id', sa.String(255), nullable=False),
        sa.Column('evaluator_id', sa.String(255), nullable=False),
        sa.Column('evaluation_type', sa.String(100), nullable=False),
        sa.Column('evaluation_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('technical_skills', sa.JSON(), nullable=True),
        sa.Column('soft_skills', sa.JSON(), nullable=True),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('recommendations', sa.Text(), nullable=True),
        sa.Column('areas_for_improvement', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('strengths', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('is_submitted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['softwarefactoryservice_schema.projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sprint_id'], ['softwarefactoryservice_schema.sprints.id'], ondelete='SET NULL'),
        schema='softwarefactoryservice_schema'
    )
    
    # Índices para consultas de evaluación
    op.create_index('idx_evaluations_student', 'evaluations', ['student_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_evaluations_evaluator', 'evaluations', ['evaluator_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_evaluations_project', 'evaluations', ['project_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_evaluations_sprint', 'evaluations', ['sprint_id'], schema='softwarefactoryservice_schema')
    op.create_index('idx_evaluations_date', 'evaluations', ['evaluation_date'], schema='softwarefactoryservice_schema')
    op.create_index('idx_evaluations_submitted', 'evaluations', ['is_submitted', 'evaluation_date'], schema='softwarefactoryservice_schema')
    op.create_index('idx_evaluations_student_project', 'evaluations', ['student_id', 'project_id'], schema='softwarefactoryservice_schema')


def downgrade() -> None:
    # Eliminar tablas en orden inverso para respetar foreign keys
    op.execute("SET search_path TO softwarefactoryservice_schema")
    
    op.drop_table('evaluations', schema='softwarefactoryservice_schema')
    op.drop_table('user_stories', schema='softwarefactoryservice_schema')
    op.drop_table('sprints', schema='softwarefactoryservice_schema')
    op.drop_table('team_members', schema='softwarefactoryservice_schema')
    op.drop_table('teams', schema='softwarefactoryservice_schema')
    op.drop_table('technologies', schema='softwarefactoryservice_schema')
    op.drop_table('projects', schema='softwarefactoryservice_schema')
