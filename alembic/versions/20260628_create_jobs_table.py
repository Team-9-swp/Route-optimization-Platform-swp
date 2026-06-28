"""create jobs table

Revision ID: 20260628_create_jobs_table
Revises:
Create Date: 2026-06-28 14:47:35.833000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260628_create_jobs_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'jobs',
        sa.Column('job_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('seed', sa.Integer, nullable=False),
        sa.Column('time_limit', sa.Float, nullable=True),
        sa.Column('input_data', sa.JSON, nullable=False),
        sa.Column('result', sa.JSON, nullable=True),
        sa.Column('error', sa.Text, nullable=True),
        sa.Column('objective_value', sa.Float, nullable=True),
        sa.Column('validation_status', sa.String(20), nullable=True),
        sa.Column('validation_report', sa.JSON, nullable=True),
        sa.PrimaryKeyConstraint('job_id'),
    )


def downgrade() -> None:
    op.drop_table('jobs')
