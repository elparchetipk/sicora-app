"""Alembic environment configuration for SoftwareFactoryService.

This module configures Alembic for database migrations in the SoftwareFactoryService,
ensuring proper schema management and version control for the software factory
database. This service coordinates with the Go implementation of SoftwareFactoryService.
"""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, MetaData, Table, Column, String, DateTime, Integer, Boolean, Text, ForeignKey
from alembic import context

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define the schema for this service
SCHEMA_NAME = "softwarefactoryservice_schema"

# Define metadata with Go GORM entities structure
# This matches the entities defined in the Go microservice
metadata = MetaData(schema=SCHEMA_NAME)

# Project table
projects = Table(
    'projects', metadata,
    Column('id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('name', String(255), nullable=False),
    Column('description', Text),
    Column('instructor_id', String(100), nullable=False),
    Column('course_id', String(100), nullable=False),
    Column('status', String(50), nullable=False),
    Column('start_date', DateTime, nullable=False),
    Column('end_date', DateTime, nullable=False),
    Column('client_info', Text),  # JSON
    Column('complexity_level', String(50), nullable=False),
    Column('evaluation_criteria', Text),  # JSON
    Column('deliverables', Text),  # JSON
    Column('milestones', Text),  # JSON
    Column('repository_url', String(500)),
    Column('demo_url', String(500)),
    Column('documentation_url', String(500)),
    Column('is_active', Boolean, default=True),
    Column('tags', Text),  # JSON
)

# Team table
teams = Table(
    'teams', metadata,
    Column('id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('name', String(255), nullable=False),
    Column('description', Text),
    Column('project_id', String, ForeignKey(f'{SCHEMA_NAME}.projects.id'), nullable=False),
    Column('leader_id', String(100), nullable=False),
    Column('max_members', Integer, default=6),
    Column('current_size', Integer, default=0),
    Column('formation_date', DateTime, nullable=False),
    Column('is_active', Boolean, default=True),
    Column('rotation_schedule', Text),  # JSON
)

# Team Members table
team_members = Table(
    'team_members', metadata,
    Column('id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('team_id', String, ForeignKey(f'{SCHEMA_NAME}.teams.id'), nullable=False),
    Column('user_id', String(100), nullable=False),
    Column('role_focus', String(100), nullable=False),
    Column('joined_at', DateTime, nullable=False),
    Column('is_active', Boolean, default=True),
)

# Sprint table
sprints = Table(
    'sprints', metadata,
    Column('id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('project_id', String, ForeignKey(f'{SCHEMA_NAME}.projects.id'), nullable=False),
    Column('name', String(255), nullable=False),
    Column('goal', Text),
    Column('start_date', DateTime, nullable=False),
    Column('end_date', DateTime, nullable=False),
    Column('status', String(50), nullable=False),
    Column('velocity', Integer, default=0),
    Column('completed_stories', Integer, default=0),
    Column('total_stories', Integer, default=0),
    Column('retrospective_notes', Text),
    Column('is_current', Boolean, default=False),
)

# User Story table
user_stories = Table(
    'user_stories', metadata,
    Column('id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('project_id', String, ForeignKey(f'{SCHEMA_NAME}.projects.id'), nullable=False),
    Column('sprint_id', String, ForeignKey(f'{SCHEMA_NAME}.sprints.id')),
    Column('title', String(255), nullable=False),
    Column('description', Text),
    Column('assignee_id', String(100)),
    Column('status', String(50), nullable=False),
    Column('priority', Integer, default=1),
    Column('story_points', Integer),
    Column('acceptance_criteria', Text),  # JSON
    Column('academic_criteria', Text),  # JSON
    Column('technical_notes', Text),
    Column('business_value', Integer, default=1),
    Column('dependencies', Text),  # JSON
    Column('tags', String(500)),
    Column('estimated_hours', Integer),
    Column('actual_hours', Integer),
)

# Evaluation table
evaluations = Table(
    'evaluations', metadata,
    Column('id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('project_id', String, ForeignKey(f'{SCHEMA_NAME}.projects.id'), nullable=False),
    Column('sprint_id', String, ForeignKey(f'{SCHEMA_NAME}.sprints.id')),
    Column('user_story_id', String, ForeignKey(f'{SCHEMA_NAME}.user_stories.id')),
    Column('student_id', String(100), nullable=False),
    Column('evaluator_id', String(100), nullable=False),
    Column('evaluation_type', String(50), nullable=False),
    Column('evaluation_date', DateTime, nullable=False),
    Column('technical_skills', Text),  # JSON
    Column('soft_skills', Text),  # JSON
    Column('overall_score', Integer),
    Column('feedback', Text),
    Column('recommendations', Text),
    Column('strengths', Text),
    Column('improvement_areas', Text),
    Column('status', String(50), nullable=False),
    Column('is_final', Boolean, default=False),
)

# Technology table
technologies = Table(
    'technologies', metadata,
    Column('id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('deleted_at', DateTime),
    Column('name', String(255), nullable=False),
    Column('description', Text),
    Column('category', String(100), nullable=False),
    Column('version', String(50)),
    Column('level', String(50), nullable=False),
    Column('is_active', Boolean, default=True),
    Column('documentation_url', String(500)),
    Column('learning_resources', Text),  # JSON
    Column('prerequisites', String(500)),
    Column('license_type', String(100)),
    Column('usage_count', Integer, default=0),
    Column('tags', String(500)),
)

# Set target metadata
target_metadata = metadata

def get_url():
    """Get database URL from environment or config."""
    return os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=SCHEMA_NAME,
        version_table="alembic_version_softwarefactoryservice",
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Create schema if it doesn't exist
        connection.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")
        connection.commit()
        
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=SCHEMA_NAME,
            version_table="alembic_version_softwarefactoryservice",
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
