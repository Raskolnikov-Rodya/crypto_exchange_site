"""add order wallet withdrawal queue tables

Revision ID: c1b2d3e4f5a6
Revises: 8ffbc3562fe8
Create Date: 2026-02-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c1b2d3e4f5a6"
down_revision: Union[str, Sequence[str], None] = "8ffbc3562fe8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return table_name in inspector.get_table_names()


def _column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def upgrade() -> None:
    if not _table_exists("orders"):
        op.create_table(
            "orders",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("side", sa.String(length=10), nullable=False),
            sa.Column("symbol", sa.String(length=20), nullable=False),
            sa.Column("price", sa.Numeric(precision=36, scale=18), nullable=False),
            sa.Column("amount", sa.Numeric(precision=36, scale=18), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False, server_default="open"),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)
        op.create_index(op.f("ix_orders_symbol"), "orders", ["symbol"], unique=False)
        op.create_index(op.f("ix_orders_user_id"), "orders", ["user_id"], unique=False)

    if not _table_exists("wallets"):
        op.create_table(
            "wallets",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("currency", sa.String(length=10), nullable=False),
            sa.Column("address", sa.String(length=255), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("address"),
        )
        op.create_index(op.f("ix_wallets_currency"), "wallets", ["currency"], unique=False)
        op.create_index(op.f("ix_wallets_id"), "wallets", ["id"], unique=False)
        op.create_index(op.f("ix_wallets_user_id"), "wallets", ["user_id"], unique=False)

    if not _table_exists("withdrawal_queue"):
        op.create_table(
            "withdrawal_queue",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("coin", sa.String(length=10), nullable=False),
            sa.Column("amount", sa.Numeric(precision=36, scale=18), nullable=False),
            sa.Column("destination_address", sa.String(length=255), nullable=False),
            sa.Column("status", sa.String(length=30), nullable=False, server_default="pending"),
            sa.Column("note", sa.String(length=255), nullable=True),
            sa.Column("tx_hash", sa.String(length=255), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_withdrawal_queue_id"), "withdrawal_queue", ["id"], unique=False)
        op.create_index(op.f("ix_withdrawal_queue_user_id"), "withdrawal_queue", ["user_id"], unique=False)
    else:
        for col in [
            sa.Column("note", sa.String(length=255), nullable=True),
            sa.Column("tx_hash", sa.String(length=255), nullable=True),
            sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        ]:
            if not _column_exists("withdrawal_queue", col.name):
                op.add_column("withdrawal_queue", col)


def downgrade() -> None:
    if _table_exists("withdrawal_queue"):
        for idx in [op.f("ix_withdrawal_queue_user_id"), op.f("ix_withdrawal_queue_id")]:
            try:
                op.drop_index(idx, table_name="withdrawal_queue")
            except Exception:
                pass
        op.drop_table("withdrawal_queue")

    if _table_exists("wallets"):
        for idx in [op.f("ix_wallets_user_id"), op.f("ix_wallets_id"), op.f("ix_wallets_currency")]:
            try:
                op.drop_index(idx, table_name="wallets")
            except Exception:
                pass
        op.drop_table("wallets")

    if _table_exists("orders"):
        for idx in [op.f("ix_orders_user_id"), op.f("ix_orders_symbol"), op.f("ix_orders_id")]:
            try:
                op.drop_index(idx, table_name="orders")
            except Exception:
                pass
        op.drop_table("orders")
