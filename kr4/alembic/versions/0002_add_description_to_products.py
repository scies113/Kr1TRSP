"""Добавление поля description в таблицу products

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавление столбца description (NOT NULL, server_default чтобы не нарушить
    # существующие строки, вставленные в первой миграции)
    op.add_column(
        "products",
        sa.Column(
            "description",
            sa.String(500),
            nullable=False,
            server_default="",
        ),
    )


def downgrade() -> None:
    op.drop_column("products", "description")
