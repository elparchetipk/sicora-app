"""Add pagination optimization indexes and constraints

Revision ID: 002_pagination_optimization
Revises: 001_initial_softwarefactory
Create Date: 2025-06-29 23:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002_pagination_optimization'
down_revision: Union[str, None] = '001_initial_softwarefactory'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Asegurar que estamos trabajando en el esquema correcto
    op.execute("SET search_path TO softwarefactoryservice_schema")
    
    # ###############################################
    # ÍNDICES COMPUESTOS PARA PAGINACIÓN EFICIENTE
    # ###############################################
    
    # Índices para paginación con ORDER BY + WHERE combinados
    # Estos índices son críticos para evitar tabla scans en consultas paginadas
    
    # Projects - Paginación por instructor con filtros
    op.create_index('idx_projects_pagination_instructor', 'projects', 
                   ['instructor_id', 'status', 'created_at', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # Projects - Paginación por curso con filtros
    op.create_index('idx_projects_pagination_course', 'projects', 
                   ['course_id', 'status', 'created_at', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # User Stories - Paginación por proyecto con estado y prioridad
    op.create_index('idx_user_stories_pagination_project', 'user_stories', 
                   ['project_id', 'status', 'priority', 'created_at', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # User Stories - Paginación por sprint
    op.create_index('idx_user_stories_pagination_sprint', 'user_stories', 
                   ['sprint_id', 'status', 'priority', 'created_at', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # User Stories - Paginación por assignee
    op.create_index('idx_user_stories_pagination_assignee', 'user_stories', 
                   ['assignee_id', 'status', 'created_at', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # Evaluations - Paginación por estudiante con fecha
    op.create_index('idx_evaluations_pagination_student', 'evaluations', 
                   ['student_id', 'evaluation_date', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # Evaluations - Paginación por evaluador con fecha
    op.create_index('idx_evaluations_pagination_evaluator', 'evaluations', 
                   ['evaluator_id', 'evaluation_date', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # Evaluations - Paginación por proyecto con fecha
    op.create_index('idx_evaluations_pagination_project', 'evaluations', 
                   ['project_id', 'evaluation_date', 'is_submitted', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # Teams - Paginación con filtros
    op.create_index('idx_teams_pagination', 'teams', 
                   ['project_id', 'created_at', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # Sprints - Paginación cronológica por proyecto
    op.create_index('idx_sprints_pagination', 'sprints', 
                   ['project_id', 'number', 'start_date', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # Technologies - Paginación por categoría
    op.create_index('idx_technologies_pagination', 'technologies', 
                   ['category', 'learning_difficulty', 'name', 'id'], 
                   schema='softwarefactoryservice_schema')
    
    # ###############################################
    # ÍNDICES PARA BÚSQUEDA DE TEXTO
    # ###############################################
    
    # Índices GIN para búsqueda de texto en campos relevantes
    op.execute("""
        CREATE INDEX idx_projects_text_search ON softwarefactoryservice_schema.projects 
        USING gin(to_tsvector('spanish', coalesce(name, '') || ' ' || coalesce(description, '')));
    """)
    
    op.execute("""
        CREATE INDEX idx_user_stories_text_search ON softwarefactoryservice_schema.user_stories 
        USING gin(to_tsvector('spanish', coalesce(title, '') || ' ' || coalesce(description, '')));
    """)
    
    op.execute("""
        CREATE INDEX idx_technologies_text_search ON softwarefactoryservice_schema.technologies 
        USING gin(to_tsvector('spanish', coalesce(name, '') || ' ' || coalesce(description, '')));
    """)
    
    # ###############################################
    # CONSTRAINTS PARA INTEGRIDAD DE DATOS
    # ###############################################
    
    # Constraint para fechas válidas en proyectos
    op.create_check_constraint(
        'chk_project_dates',
        'projects',
        'start_date <= end_date OR end_date IS NULL',
        schema='softwarefactoryservice_schema'
    )
    
    # Constraint para fechas válidas en sprints
    op.create_check_constraint(
        'chk_sprint_dates',
        'sprints',
        'start_date < end_date',
        schema='softwarefactoryservice_schema'
    )
    
    # Constraint para prioridad válida en user stories
    op.create_check_constraint(
        'chk_user_story_priority',
        'user_stories',
        'priority >= 1 AND priority <= 5',
        schema='softwarefactoryservice_schema'
    )
    
    # Constraint para story points válidos
    op.create_check_constraint(
        'chk_user_story_points',
        'user_stories',
        'story_points >= 1 AND story_points <= 21',
        schema='softwarefactoryservice_schema'
    )
    
    # Constraint para business value válido
    op.create_check_constraint(
        'chk_business_value',
        'user_stories',
        'business_value >= 1 AND business_value <= 100',
        schema='softwarefactoryservice_schema'
    )
    
    # Constraint para score válido en evaluaciones
    op.create_check_constraint(
        'chk_evaluation_score',
        'evaluations',
        'overall_score >= 0.0 AND overall_score <= 5.0',
        schema='softwarefactoryservice_schema'
    )
    
    # Constraint para tamaño de equipo válido
    op.create_check_constraint(
        'chk_team_size',
        'teams',
        'current_size >= 0 AND current_size <= max_members',
        schema='softwarefactoryservice_schema'
    )
    
    # ###############################################
    # ESTADÍSTICAS PARA OPTIMIZACIÓN
    # ###############################################
    
    # Establecer estadísticas para columnas de filtrado frecuente
    op.execute("ALTER TABLE softwarefactoryservice_schema.projects ALTER COLUMN status SET STATISTICS 1000;")
    op.execute("ALTER TABLE softwarefactoryservice_schema.projects ALTER COLUMN instructor_id SET STATISTICS 1000;")
    op.execute("ALTER TABLE softwarefactoryservice_schema.projects ALTER COLUMN course_id SET STATISTICS 1000;")
    
    op.execute("ALTER TABLE softwarefactoryservice_schema.user_stories ALTER COLUMN status SET STATISTICS 1000;")
    op.execute("ALTER TABLE softwarefactoryservice_schema.user_stories ALTER COLUMN project_id SET STATISTICS 1000;")
    op.execute("ALTER TABLE softwarefactoryservice_schema.user_stories ALTER COLUMN assignee_id SET STATISTICS 1000;")
    
    op.execute("ALTER TABLE softwarefactoryservice_schema.evaluations ALTER COLUMN student_id SET STATISTICS 1000;")
    op.execute("ALTER TABLE softwarefactoryservice_schema.evaluations ALTER COLUMN evaluator_id SET STATISTICS 1000;")
    op.execute("ALTER TABLE softwarefactoryservice_schema.evaluations ALTER COLUMN project_id SET STATISTICS 1000;")


def downgrade() -> None:
    # Eliminar en orden inverso
    op.execute("SET search_path TO softwarefactoryservice_schema")
    
    # Eliminar constraints
    op.drop_constraint('chk_team_size', 'teams', schema='softwarefactoryservice_schema')
    op.drop_constraint('chk_evaluation_score', 'evaluations', schema='softwarefactoryservice_schema')
    op.drop_constraint('chk_business_value', 'user_stories', schema='softwarefactoryservice_schema')
    op.drop_constraint('chk_user_story_points', 'user_stories', schema='softwarefactoryservice_schema')
    op.drop_constraint('chk_user_story_priority', 'user_stories', schema='softwarefactoryservice_schema')
    op.drop_constraint('chk_sprint_dates', 'sprints', schema='softwarefactoryservice_schema')
    op.drop_constraint('chk_project_dates', 'projects', schema='softwarefactoryservice_schema')
    
    # Eliminar índices de texto
    op.drop_index('idx_technologies_text_search', schema='softwarefactoryservice_schema')
    op.drop_index('idx_user_stories_text_search', schema='softwarefactoryservice_schema')
    op.drop_index('idx_projects_text_search', schema='softwarefactoryservice_schema')
    
    # Eliminar índices de paginación
    op.drop_index('idx_technologies_pagination', schema='softwarefactoryservice_schema')
    op.drop_index('idx_sprints_pagination', schema='softwarefactoryservice_schema')
    op.drop_index('idx_teams_pagination', schema='softwarefactoryservice_schema')
    op.drop_index('idx_evaluations_pagination_project', schema='softwarefactoryservice_schema')
    op.drop_index('idx_evaluations_pagination_evaluator', schema='softwarefactoryservice_schema')
    op.drop_index('idx_evaluations_pagination_student', schema='softwarefactoryservice_schema')
    op.drop_index('idx_user_stories_pagination_assignee', schema='softwarefactoryservice_schema')
    op.drop_index('idx_user_stories_pagination_sprint', schema='softwarefactoryservice_schema')
    op.drop_index('idx_user_stories_pagination_project', schema='softwarefactoryservice_schema')
    op.drop_index('idx_projects_pagination_course', schema='softwarefactoryservice_schema')
    op.drop_index('idx_projects_pagination_instructor', schema='softwarefactoryservice_schema')
