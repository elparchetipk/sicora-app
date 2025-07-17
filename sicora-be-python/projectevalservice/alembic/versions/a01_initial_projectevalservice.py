"""Initial migration for projectevalservice

Revision ID: 001_initial
Revises: 
Create Date: 2025-06-29 05:59:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a01_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM types in the correct schema
    op.execute("CREATE TYPE projectevalservice_schema.projectstatus AS ENUM ('IDEA_PROPOSAL', 'APPROVED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')")
    op.execute("CREATE TYPE projectevalservice_schema.projecttype AS ENUM ('FORMATIVE', 'PRODUCTIVE', 'RESEARCH', 'INNOVATION')")
    op.execute("CREATE TYPE projectevalservice_schema.evaluationstatus AS ENUM ('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')")
    op.execute("CREATE TYPE projectevalservice_schema.evaluationtype AS ENUM ('INITIAL', 'INTERMEDIATE', 'FINAL', 'FOLLOW_UP')")
    op.execute("CREATE TYPE projectevalservice_schema.stakeholderstatus AS ENUM ('ACTIVE', 'INACTIVE', 'PENDING')")
    op.execute("CREATE TYPE projectevalservice_schema.stakeholdertype AS ENUM ('INDUSTRY', 'ACADEMIC', 'GOVERNMENT', 'NGO', 'COMMUNITY')")
    
    # Create projects table
    op.create_table('projects',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', postgresql.ENUM('IDEA_PROPOSAL', 'APPROVED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='projectstatus', schema='projectevalservice_schema'), nullable=False),
        sa.Column('project_type', postgresql.ENUM('FORMATIVE', 'PRODUCTIVE', 'RESEARCH', 'INNOVATION', name='projecttype', schema='projectevalservice_schema'), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('budget', sa.Float(), nullable=True),
        sa.Column('stakeholder_requirements', sa.JSON(), nullable=True),
        sa.Column('technology_stack', sa.JSON(), nullable=True),
        sa.Column('deliverables', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        schema='projectevalservice_schema'
    )
    
    # Create stakeholders table
    op.create_table('stakeholders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('stakeholder_type', postgresql.ENUM('INDUSTRY', 'ACADEMIC', 'GOVERNMENT', 'NGO', 'COMMUNITY', name='stakeholdertype', schema='projectevalservice_schema'), nullable=False),
        sa.Column('status', postgresql.ENUM('ACTIVE', 'INACTIVE', 'PENDING', name='stakeholderstatus', schema='projectevalservice_schema'), nullable=False),
        sa.Column('contact_person', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('organization_size', sa.String(length=50), nullable=True),
        sa.Column('sector', sa.String(length=100), nullable=True),
        sa.Column('website', sa.String(length=500), nullable=True),
        sa.Column('capabilities', sa.JSON(), nullable=True),
        sa.Column('requirements', sa.JSON(), nullable=True),
        sa.Column('partnership_history', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        schema='projectevalservice_schema'
    )
    
    # Create evaluations table
    op.create_table('evaluations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('evaluation_type', postgresql.ENUM('INITIAL', 'INTERMEDIATE', 'FINAL', 'FOLLOW_UP', name='evaluationtype', schema='projectevalservice_schema'), nullable=False),
        sa.Column('status', postgresql.ENUM('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='evaluationstatus', schema='projectevalservice_schema'), nullable=False),
        sa.Column('evaluator_id', sa.String(length=255), nullable=False),
        sa.Column('scheduled_date', sa.DateTime(), nullable=False),
        sa.Column('completed_date', sa.DateTime(), nullable=True),
        sa.Column('criteria', sa.JSON(), nullable=True),
        sa.Column('scores', sa.JSON(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('recommendations', sa.Text(), nullable=True),
        sa.Column('attachments', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['project_id'], ['projectevalservice_schema.projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='projectevalservice_schema'
    )
    
    # Create indexes
    op.create_index('ix_projects_status', 'projects', ['status'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_projects_type', 'projects', ['project_type'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_projects_active', 'projects', ['is_active'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_projects_created_at', 'projects', ['created_at'], unique=False, schema='projectevalservice_schema')
    
    op.create_index('ix_stakeholders_email', 'stakeholders', ['email'], unique=True, schema='projectevalservice_schema')
    op.create_index('ix_stakeholders_type', 'stakeholders', ['stakeholder_type'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_stakeholders_status', 'stakeholders', ['status'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_stakeholders_active', 'stakeholders', ['is_active'], unique=False, schema='projectevalservice_schema')
    
    op.create_index('ix_evaluations_project_id', 'evaluations', ['project_id'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_evaluations_status', 'evaluations', ['status'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_evaluations_type', 'evaluations', ['evaluation_type'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_evaluations_evaluator', 'evaluations', ['evaluator_id'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_evaluations_scheduled_date', 'evaluations', ['scheduled_date'], unique=False, schema='projectevalservice_schema')
    op.create_index('ix_evaluations_active', 'evaluations', ['is_active'], unique=False, schema='projectevalservice_schema')


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_evaluations_active', table_name='evaluations', schema='projectevalservice_schema')
    op.drop_index('ix_evaluations_scheduled_date', table_name='evaluations', schema='projectevalservice_schema')
    op.drop_index('ix_evaluations_evaluator', table_name='evaluations', schema='projectevalservice_schema')
    op.drop_index('ix_evaluations_type', table_name='evaluations', schema='projectevalservice_schema')
    op.drop_index('ix_evaluations_status', table_name='evaluations', schema='projectevalservice_schema')
    op.drop_index('ix_evaluations_project_id', table_name='evaluations', schema='projectevalservice_schema')
    
    op.drop_index('ix_stakeholders_active', table_name='stakeholders', schema='projectevalservice_schema')
    op.drop_index('ix_stakeholders_status', table_name='stakeholders', schema='projectevalservice_schema')
    op.drop_index('ix_stakeholders_type', table_name='stakeholders', schema='projectevalservice_schema')
    op.drop_index('ix_stakeholders_email', table_name='stakeholders', schema='projectevalservice_schema')
    
    op.drop_index('ix_projects_created_at', table_name='projects', schema='projectevalservice_schema')
    op.drop_index('ix_projects_active', table_name='projects', schema='projectevalservice_schema')
    op.drop_index('ix_projects_type', table_name='projects', schema='projectevalservice_schema')
    op.drop_index('ix_projects_status', table_name='projects', schema='projectevalservice_schema')
    
    # Drop tables
    op.drop_table('evaluations', schema='projectevalservice_schema')
    op.drop_table('stakeholders', schema='projectevalservice_schema')
    op.drop_table('projects', schema='projectevalservice_schema')
    
    # Drop ENUM types
    op.execute("DROP TYPE IF EXISTS projectevalservice_schema.stakeholdertype")
    op.execute("DROP TYPE IF EXISTS projectevalservice_schema.stakeholderstatus")
    op.execute("DROP TYPE IF EXISTS projectevalservice_schema.evaluationtype")
    op.execute("DROP TYPE IF EXISTS projectevalservice_schema.evaluationstatus")
    op.execute("DROP TYPE IF EXISTS projectevalservice_schema.projecttype")
    op.execute("DROP TYPE IF EXISTS projectevalservice_schema.projectstatus")
