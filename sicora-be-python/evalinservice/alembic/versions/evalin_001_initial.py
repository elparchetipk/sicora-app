"""Create EvalinService tables

Revision ID: evalin_001_initial
Revises: 
Create Date: 2025-06-13 00:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'evalin_001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all EvalinService tables."""
    
    # Questions table
    op.create_table('questions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('text', sa.String(length=500), nullable=False),
        sa.Column('type', sa.Enum('SCALE_1_5', 'TEXT', 'MULTIPLE_CHOICE', name='questiontype'), nullable=False),
        sa.Column('options', sa.JSON(), nullable=True),
        sa.Column('is_required', sa.Boolean(), nullable=False, default=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('length(text) >= 10', name='min_text_length'),
        sa.CheckConstraint('length(text) <= 500', name='max_text_length')
    )
    op.create_index(op.f('ix_questions_type'), 'questions', ['type'], unique=False)
    op.create_index(op.f('ix_questions_is_required'), 'questions', ['is_required'], unique=False)
    
    # Questionnaires table
    op.create_table('questionnaires',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('length(name) >= 5', name='min_name_length'),
        sa.CheckConstraint('length(name) <= 200', name='max_name_length')
    )
    op.create_index(op.f('ix_questionnaires_name'), 'questionnaires', ['name'], unique=False)
    op.create_index(op.f('ix_questionnaires_is_active'), 'questionnaires', ['is_active'], unique=False)
    
    # Questionnaire Questions association table
    op.create_table('questionnaire_questions',
        sa.Column('questionnaire_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('question_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['questionnaire_id'], ['questionnaires.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('questionnaire_id', 'question_id'),
        sa.UniqueConstraint('questionnaire_id', 'order', name='unique_question_order_per_questionnaire')
    )
    
    # Evaluation Periods table
    op.create_table('evaluation_periods',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('questionnaire_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.Enum('SCHEDULED', 'ACTIVE', 'COMPLETED', 'CANCELLED', name='periodstatus'), nullable=False, default='SCHEDULED'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['questionnaire_id'], ['questionnaires.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('end_date > start_date', name='valid_date_range'),
        sa.CheckConstraint('length(name) >= 5', name='min_period_name_length'),
        sa.CheckConstraint('length(name) <= 200', name='max_period_name_length')
    )
    op.create_index(op.f('ix_evaluation_periods_name'), 'evaluation_periods', ['name'], unique=False)
    op.create_index(op.f('ix_evaluation_periods_status'), 'evaluation_periods', ['status'], unique=False)
    op.create_index(op.f('ix_evaluation_periods_start_date'), 'evaluation_periods', ['start_date'], unique=False)
    op.create_index(op.f('ix_evaluation_periods_end_date'), 'evaluation_periods', ['end_date'], unique=False)
    
    # Evaluations table
    op.create_table('evaluations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('instructor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('period_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('responses', sa.JSON(), nullable=False),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('DRAFT', 'SUBMITTED', name='evaluationstatus'), nullable=False, default='DRAFT'),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['period_id'], ['evaluation_periods.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id', 'instructor_id', 'period_id', name='unique_student_instructor_period'),
        sa.CheckConstraint('(status = \'SUBMITTED\' AND submitted_at IS NOT NULL) OR (status = \'DRAFT\')', name='submitted_status_consistency')
    )
    op.create_index(op.f('ix_evaluations_student_id'), 'evaluations', ['student_id'], unique=False)
    op.create_index(op.f('ix_evaluations_instructor_id'), 'evaluations', ['instructor_id'], unique=False)
    op.create_index(op.f('ix_evaluations_status'), 'evaluations', ['status'], unique=False)
    op.create_index(op.f('ix_evaluations_submitted_at'), 'evaluations', ['submitted_at'], unique=False)


def downgrade() -> None:
    """Drop all EvalinService tables."""
    
    # Drop tables in reverse order to handle foreign key constraints
    op.drop_table('evaluations')
    op.drop_table('evaluation_periods')
    op.drop_table('questionnaire_questions')
    op.drop_table('questionnaires')
    op.drop_table('questions')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS evaluationstatus')
    op.execute('DROP TYPE IF EXISTS periodstatus')
    op.execute('DROP TYPE IF EXISTS questiontype')
