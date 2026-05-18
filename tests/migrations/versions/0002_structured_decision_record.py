"""structured decision record

Revision ID: 0002_structured_decision_record
Revises: 0001_initial_mvp_core
Create Date: 2026-05-15
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_structured_decision_record"
down_revision = "0001_initial_mvp_core"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("decision_records", sa.Column("record_data", sa.JSON(), nullable=True))


def downgrade():
    op.drop_column("decision_records", "record_data")
