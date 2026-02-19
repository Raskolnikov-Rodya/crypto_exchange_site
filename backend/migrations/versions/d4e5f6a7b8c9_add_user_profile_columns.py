"""add username and phone to users

Revision ID: d4e5f6a7b8c9
Revises: c1b2d3e4f5a6
Create Date: 2026-02-19 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "c1b2d3e4f5a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def _index_exists(table_name: str, index_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return any(idx["name"] == index_name for idx in inspector.get_indexes(table_name))


def upgrade() -> None:
    if not _column_exists("users", "username"):
        op.add_column("users", sa.Column("username", sa.String(length=50), nullable=True))
    if not _column_exists("users", "phone"):
        op.add_column("users", sa.Column("phone", sa.String(length=25), nullable=True))

    if not _index_exists("users", "ix_users_username"):
        op.create_index("ix_users_username", "users", ["username"], unique=True)


def downgrade() -> None:
    try:
        op.drop_index("ix_users_username", table_name="users")
    except Exception:
        pass

    if _column_exists("users", "phone"):
        op.drop_column("users", "phone")
    if _column_exists("users", "username"):
        op.drop_column("users", "username")
