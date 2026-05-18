"""decision context objects

Revision ID: 0004_decision_context_objects
Revises: 0003_merge_alembic_heads
Create Date: 2026-05-15
"""
from alembic import op
import sqlalchemy as sa

revision = "0004_decision_context_objects"
down_revision = "31307c981c0a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "decision_context_objects",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("decision_id", sa.String(length=36), nullable=False),
        sa.Column("scenario_id", sa.String(length=36), nullable=True),
        sa.Column("context_type", sa.String(length=40), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=200), nullable=True),
        sa.Column("owner", sa.String(length=120), nullable=True),
        sa.Column("confidence", sa.String(length=20), nullable=False),
        sa.Column("valid_from", sa.DateTime(), nullable=True),
        sa.Column("valid_to", sa.DateTime(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["decision_id"], ["decisions.id"]),
        sa.ForeignKeyConstraint(["scenario_id"], ["scenarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_decision_context_objects_decision_type", "decision_context_objects", ["decision_id", "context_type"])


def downgrade():
    op.drop_index("ix_decision_context_objects_decision_type", table_name="decision_context_objects")
    op.drop_table("decision_context_objects")
