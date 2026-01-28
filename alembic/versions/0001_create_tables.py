"""create tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2026-01-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_create_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.UniqueConstraint("address", name="uq_buildings_address"),
    )
    op.create_index("ix_buildings_address", "buildings", ["address"], unique=True)

    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("activities.id"), nullable=True),
        sa.CheckConstraint("level >= 1 AND level <= 3", name="ck_activity_level"),
    )
    op.create_index("ix_activities_name", "activities", ["name"], unique=False)

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("building_id", sa.Integer(), sa.ForeignKey("buildings.id"), nullable=False),
    )
    op.create_index("ix_organizations_name", "organizations", ["name"], unique=False)

    op.create_table(
        "organization_phones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
    )

    op.create_table(
        "organization_activities",
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), primary_key=True),
        sa.Column("activity_id", sa.Integer(), sa.ForeignKey("activities.id"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("organization_activities")
    op.drop_table("organization_phones")
    op.drop_index("ix_organizations_name", table_name="organizations")
    op.drop_table("organizations")
    op.drop_index("ix_activities_name", table_name="activities")
    op.drop_table("activities")
    op.drop_index("ix_buildings_address", table_name="buildings")
    op.drop_table("buildings")
