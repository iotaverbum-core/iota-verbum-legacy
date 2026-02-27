"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2026-02-19
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "seasonentry",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("device_id", sa.String(), nullable=False),
        sa.Column("text_hash", sa.String(), nullable=False),
        sa.Column("modal", sa.JSON(), nullable=False),
        sa.Column("hinge_action", sa.String(), nullable=False),
        sa.Column("eden_text", sa.Text(), nullable=True),
        sa.Column("attestation", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "momententry",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("device_id", sa.String(), nullable=False),
        sa.Column("text_hash", sa.String(), nullable=False),
        sa.Column("modal", sa.JSON(), nullable=False),
        sa.Column("hinge_action", sa.String(), nullable=False),
        sa.Column("eden_text", sa.Text(), nullable=True),
        sa.Column("attestation", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("momententry")
    op.drop_table("seasonentry")
