"""observation and reassessment slice

Revision ID: 0002_observation_reassessment
Revises: 0001_initial_mvp_core
Create Date: 2026-05-15
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_observation_reassessment"
down_revision = "0001_initial_mvp_core"
branch_labels = None
depends_on = None


def governance_columns():
    return [
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
    ]


def upgrade():
    op.create_table(
        "observation_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("decision_id", sa.String(length=36), nullable=False),
        sa.Column("expected_benefit", sa.Numeric(12, 2), nullable=False),
        sa.Column("actual_benefit", sa.Numeric(12, 2), nullable=False),
        sa.Column("expected_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("actual_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("expected_risks", sa.Text(), nullable=True),
        sa.Column("actual_risks", sa.Text(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        *governance_columns(),
        sa.ForeignKeyConstraint(["decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("observation_records")
