"""create_attendance_tables

Revision ID: 001
Revises: 
Create Date: 2025-06-12 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create attendance_records table
    op.create_table('attendance_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ficha_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('class_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('status', sa.Enum('PRESENT', 'ABSENT', 'LATE', 'EXCUSED', name='attendancestatus'), nullable=False),
        sa.Column('check_in_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('check_out_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('late_minutes', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_justified', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for attendance_records
    op.create_index('idx_attendance_records_student_date', 'attendance_records', ['student_id', 'date'])
    op.create_index('idx_attendance_records_ficha_date', 'attendance_records', ['ficha_id', 'date'])
    op.create_index('idx_attendance_records_class_date', 'attendance_records', ['class_id', 'date'])
    op.create_index('idx_attendance_records_status', 'attendance_records', ['status'])
    op.create_index('idx_attendance_records_date', 'attendance_records', ['date'])

    # Create justifications table
    op.create_table('justifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('attendance_record_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('justification_type', sa.String(50), nullable=False),
        sa.Column('document_path', sa.String(500), nullable=True),
        sa.Column('document_name', sa.String(255), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='justificationstatus'), nullable=False, default='PENDING'),
        sa.Column('reviewed_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['attendance_record_id'], ['attendance_records.id'], ondelete='CASCADE')
    )
    
    # Create indexes for justifications
    op.create_index('idx_justifications_attendance_record', 'justifications', ['attendance_record_id'])
    op.create_index('idx_justifications_student', 'justifications', ['student_id'])
    op.create_index('idx_justifications_status', 'justifications', ['status'])
    op.create_index('idx_justifications_submitted_at', 'justifications', ['submitted_at'])

    # Create attendance_alerts table
    op.create_table('attendance_alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ficha_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('alert_type', sa.Enum('CONSECUTIVE_ABSENCES', 'LOW_ATTENDANCE', 'FREQUENT_LATE', 'NO_INSTRUCTOR_ATTENDANCE', name='alerttype'), nullable=False),
        sa.Column('level', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='alertlevel'), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('acknowledged', sa.Boolean(), nullable=False, default=False),
        sa.Column('acknowledged_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for attendance_alerts
    op.create_index('idx_attendance_alerts_student', 'attendance_alerts', ['student_id'])
    op.create_index('idx_attendance_alerts_ficha', 'attendance_alerts', ['ficha_id'])
    op.create_index('idx_attendance_alerts_type', 'attendance_alerts', ['alert_type'])
    op.create_index('idx_attendance_alerts_level', 'attendance_alerts', ['level'])
    op.create_index('idx_attendance_alerts_active', 'attendance_alerts', ['is_active'])
    op.create_index('idx_attendance_alerts_acknowledged', 'attendance_alerts', ['acknowledged'])
    op.create_index('idx_attendance_alerts_created_at', 'attendance_alerts', ['created_at'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('attendance_alerts')
    op.drop_table('justifications')
    op.drop_table('attendance_records')
    
    # Drop enums
    sa.Enum(name='alertlevel').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='alerttype').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='justificationstatus').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='attendancestatus').drop(op.get_bind(), checkfirst=False)
