"""initial: requests table + request_seq

Revision ID: 0001
Revises:
Create Date: 2026-01-01 00:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SEQUENCE IF NOT EXISTS request_seq START 1")
    op.create_table(
        "requests",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("channel", sa.String(length=16), nullable=False),
        sa.Column("thread_key", sa.String(length=255), nullable=False),
        sa.Column("idem_key", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="new"),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("client_contact", sa.String(length=255), nullable=True),
        sa.Column("client_id", sa.BigInteger(), nullable=True),
        sa.Column("attachment_ref", sa.String(length=512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_requests")),
        sa.UniqueConstraint("idem_key", name="uq_requests_idem_key"),
    )
    op.create_index("ix_requests_thread_key", "requests", ["thread_key"], unique=False)
    op.create_index("ix_requests_status", "requests", ["status"], unique=False)
    op.create_index("ix_requests_created_at", "requests", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_requests_created_at", table_name="requests")
    op.drop_index("ix_requests_status", table_name="requests")
    op.drop_index("ix_requests_thread_key", table_name="requests")
    op.drop_table("requests")
    op.execute("DROP SEQUENCE IF EXISTS request_seq")
