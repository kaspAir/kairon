"""Merge Alembic heads

Revision ID: 31307c981c0a
Revises: 0003_merge_alembic_heads, 8a5d7d9fba0c
Create Date: 2026-05-15 21:38:01.726727
"""
from alembic import op
import sqlalchemy as sa


revision = '31307c981c0a'
down_revision = ('0003_merge_alembic_heads', '8a5d7d9fba0c')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
