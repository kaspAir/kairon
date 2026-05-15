"""initial MVP core schema

Revision ID: 0001_initial_mvp_core
Revises:
Create Date: 2026-05-15
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_mvp_core"
down_revision = None
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
        "decisions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("context", sa.Text(), nullable=True),
        *governance_columns(),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "decision_variants",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("decision_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("estimated_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("expected_benefit", sa.Numeric(12, 2), nullable=False),
        *governance_columns(),
        sa.ForeignKeyConstraint(["decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "scenarios",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("decision_id", sa.String(length=36), nullable=False),
        sa.Column("variant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("case_volume", sa.Integer(), nullable=False),
        sa.Column("processing_minutes_per_case", sa.Numeric(12, 2), nullable=False),
        sa.Column("hourly_cost", sa.Numeric(12, 2), nullable=False),
        *governance_columns(),
        sa.ForeignKeyConstraint(["decision_id"], ["decisions.id"]),
        sa.ForeignKeyConstraint(["variant_id"], ["decision_variants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "risk_assessments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("decision_id", sa.String(length=36), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("mitigation", sa.Text(), nullable=True),
        *governance_columns(),
        sa.ForeignKeyConstraint(["decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "approval_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("decision_id", sa.String(length=36), nullable=False),
        sa.Column("approved_by", sa.String(length=120), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        *governance_columns(),
        sa.ForeignKeyConstraint(["decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "simulation_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("scenario_id", sa.String(length=36), nullable=False),
        sa.Column("total_processing_hours", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("deterministic_formula", sa.String(length=300), nullable=False),
        sa.Column("simulated_at", sa.DateTime(), nullable=False),
        *governance_columns(),
        sa.ForeignKeyConstraint(["scenario_id"], ["scenarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "impact_assessments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("simulation_run_id", sa.String(length=36), nullable=False),
        sa.Column("cost_impact", sa.Numeric(12, 2), nullable=False),
        sa.Column("benefit_impact", sa.Numeric(12, 2), nullable=False),
        sa.Column("net_impact", sa.Numeric(12, 2), nullable=False),
        sa.Column("confidence_score", sa.Numeric(4, 2), nullable=False),
        *governance_columns(),
        sa.ForeignKeyConstraint(["simulation_run_id"], ["simulation_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "decision_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("decision_id", sa.String(length=36), nullable=False),
        sa.Column("record_text", sa.Text(), nullable=False),
        *governance_columns(),
        sa.ForeignKeyConstraint(["decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("decision_records")
    op.drop_table("impact_assessments")
    op.drop_table("simulation_runs")
    op.drop_table("approval_records")
    op.drop_table("risk_assessments")
    op.drop_table("scenarios")
    op.drop_table("decision_variants")
    op.drop_table("decisions")
