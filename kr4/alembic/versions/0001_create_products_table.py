"""Создание таблицы products и вставка начальных данных

Revision ID: 0001
Revises: 
Create Date: 2026-05-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создание таблицы products (без поля description — оно будет добавлено во 2-й миграции)
    products_table_zolotov = op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False, server_default="0"),
    )

    # Вставка двух начальных записей (bulk_insert)
    op.bulk_insert(
        products_table_zolotov,
        [
            {"title": "Ноутбук ASUS", "price": 74999.99, "count": 10},
            {"title": "Мышь Logitech", "price": 2499.00, "count": 50},
        ],
    )


def downgrade() -> None:
    op.drop_table("products")
