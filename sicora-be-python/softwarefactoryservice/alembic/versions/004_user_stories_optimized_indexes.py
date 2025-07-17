"""Add optimized indexes based on user stories analysis

Revision ID: 004_user_stories_optimized_indexes
Revises: 003_analytics_optimization
Create Date: 2025-06-29 23:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_user_stories_optimized_indexes'
down_revision = '003_analytics_optimization'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add optimized indexes based on user stories analysis"""
    
    # ==========================================
    # CRÍTICOS: Alta Frecuencia - Alto Impacto
    # ==========================================
    
    # HU-002: Gestión de Backlog - CRÍTICO
    # Optimización para consultas de backlog con múltiples filtros
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_backlog_management 
        ON softwarefactoryservice_schema.factory_user_stories 
        (project_id, sprint_id, status, priority, created_at) 
        WHERE sprint_id IS NULL OR status = 'backlog'
    """)
    
    # HU-004: Dashboard Personal del Aprendiz - CRÍTICO
    # Índice parcial para tareas activas del aprendiz
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_personal_tasks 
        ON softwarefactoryservice_schema.factory_user_stories 
        (assigned_to, status, priority) 
        WHERE status IN ('todo', 'in_progress', 'review')
    """)
    
    # HU-001: Dashboard del Instructor - CRÍTICO
    # Proyectos por instructor con orden temporal
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_projects_instructor_dashboard 
        ON softwarefactoryservice_schema.factory_projects 
        (created_by, status, updated_at)
    """)
    
    # ==========================================
    # IMPORTANTES: Media Frecuencia - Alto Impacto
    # ==========================================
    
    # HU-003: Planificación de Sprint - IMPORTANTE
    # Historias disponibles para planificación
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_sprint_planning 
        ON softwarefactoryservice_schema.factory_user_stories 
        (project_id, status, priority, story_points) 
        WHERE sprint_id IS NULL AND status = 'backlog'
    """)
    
    # HU-005: Evaluación Continua - IMPORTANTE
    # Historial de evaluaciones por estudiante y proyecto
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_evaluations_comprehensive 
        ON softwarefactoryservice_schema.factory_evaluations 
        (apprentice_id, project_id, evaluation_date DESC)
    """)
    
    # Evaluaciones por rango de fechas (reportes)
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_evaluations_date_range 
        ON softwarefactoryservice_schema.factory_evaluations 
        (evaluation_date, project_id, apprentice_id)
    """)
    
    # ==========================================
    # OPTIMIZACIONES DE JOINS FRECUENTES
    # ==========================================
    
    # Join user_stories -> projects (dashboard views)
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_project_join 
        ON softwarefactoryservice_schema.factory_user_stories 
        (project_id, id, title, status)
    """)
    
    # Join user_stories -> sprints (sprint views)
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_sprint_join 
        ON softwarefactoryservice_schema.factory_user_stories 
        (sprint_id, id, story_points, status)
    """)
    
    # Join evaluations -> user_stories (evaluation reports)
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_evaluations_story_join 
        ON softwarefactoryservice_schema.factory_evaluations 
        (user_story_id, evaluation_date, overall_score)
    """)
    
    # ==========================================
    # OPTIMIZACIONES DE AGREGACIONES
    # ==========================================
    
    # HU-006: Reportes de Sprint - Métricas de velocidad
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_sprint_metrics 
        ON softwarefactoryservice_schema.factory_user_stories 
        (sprint_id, status, story_points)
    """)
    
    # Sprint analytics para evaluaciones
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_evaluations_sprint_analytics 
        ON softwarefactoryservice_schema.factory_evaluations 
        (sprint_id, overall_score, evaluation_type)
    """)
    
    # Sprint lookup optimizado para reportes
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_sprints_project_ordered 
        ON softwarefactoryservice_schema.factory_sprints 
        (project_id, sprint_number DESC, id)
    """)
    
    # ==========================================
    # OPTIMIZACIONES DE FILTRADO ESPECÍFICO
    # ==========================================
    
    # Filtrado por asignado y proyecto
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_assignee_project 
        ON softwarefactoryservice_schema.factory_user_stories 
        (assigned_to, project_id, status)
    """)
    
    # Estados para verificación de dependencias
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_dependency_status 
        ON softwarefactoryservice_schema.factory_user_stories 
        (id, status, project_id)
    """)
    
    # ==========================================
    # ÍNDICES PARCIALES PARA CASOS ESPECÍFICOS
    # ==========================================
    
    # Solo historias activas (90% de las consultas)
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_active_only 
        ON softwarefactoryservice_schema.factory_user_stories 
        (project_id, status, assigned_to)
        WHERE status NOT IN ('done', 'cancelled')
    """)
    
    # Proyectos activos únicamente
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_projects_active_only 
        ON softwarefactoryservice_schema.factory_projects 
        (created_by, complexity_level, tech_stack)
        WHERE status IN ('planning', 'active')
    """)
    
    # Sprints en curso
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_sprints_current 
        ON softwarefactoryservice_schema.factory_sprints 
        (project_id, team_id, status)
        WHERE status IN ('planning', 'active')
    """)
    
    # ==========================================
    # PAGINACIÓN OPTIMIZADA
    # ==========================================
    
    # Cursor-based pagination para user stories
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_cursor 
        ON softwarefactoryservice_schema.factory_user_stories 
        (project_id, priority, created_at, id)
    """)
    
    # Offset-based pagination con límite de estados
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_offset 
        ON softwarefactoryservice_schema.factory_user_stories 
        (project_id, status, priority, id) 
        WHERE status IN ('todo', 'in_progress', 'review', 'done')
    """)
    
    # ==========================================
    # BÚSQUEDAS CON FILTROS
    # ==========================================
    
    # HU-007: Búsqueda Global con filtros
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_search_filters 
        ON softwarefactoryservice_schema.factory_user_stories 
        (project_id, status, updated_at DESC)
    """)
    
    # ==========================================
    # SUPPORT INDEXES PARA LOOKUPS
    # ==========================================
    
    # Proyectos lookup optimizado
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_projects_active_lookup 
        ON softwarefactoryservice_schema.factory_projects 
        (id, name, status)
    """)
    
    # Sprints lookup optimizado
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_sprints_active_lookup 
        ON softwarefactoryservice_schema.factory_sprints 
        (id, sprint_number, end_date, status)
    """)
    
    # Teams para estadísticas de proyecto
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_teams_project_stats 
        ON softwarefactoryservice_schema.factory_teams 
        (project_id, is_active)
    """)
    
    # Sprints para estadísticas de proyecto
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_sprints_project_stats 
        ON softwarefactoryservice_schema.factory_sprints 
        (project_id, status)
    """)
    
    # ==========================================
    # OPTIMIZACIONES PARA ACTUALIZACIONES MASIVAS
    # ==========================================
    
    # Bulk updates durante planificación de sprint
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_factory_user_stories_bulk_update 
        ON softwarefactoryservice_schema.factory_user_stories 
        (id) 
        WHERE status IN ('backlog', 'todo')
    """)


def downgrade() -> None:
    """Remove optimized indexes based on user stories analysis"""
    
    # Drop all added indexes
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_backlog_management")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_personal_tasks")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_projects_instructor_dashboard")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_sprint_planning")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_evaluations_comprehensive")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_evaluations_date_range")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_project_join")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_sprint_join")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_evaluations_story_join")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_sprint_metrics")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_evaluations_sprint_analytics")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_sprints_project_ordered")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_assignee_project")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_dependency_status")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_active_only")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_projects_active_only")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_sprints_current")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_cursor")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_offset")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_search_filters")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_projects_active_lookup")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_sprints_active_lookup")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_teams_project_stats")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_sprints_project_stats")
    op.execute("DROP INDEX IF EXISTS softwarefactoryservice_schema.idx_factory_user_stories_bulk_update")
