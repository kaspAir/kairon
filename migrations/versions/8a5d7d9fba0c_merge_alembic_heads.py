"""merge alembic heads

Revision ID: 8a5d7d9fba0c
Revises: 0002_observation_reassessment, 0002_structured_decision_record
Create Date: 2026-05-15 20:45:19.607396
"""
from alembic import op
import sqlalchemy as sa


revision = '8a5d7d9fba0c'
down_revision = ('0002_observation_reassessment', '0002_structured_decision_record')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
