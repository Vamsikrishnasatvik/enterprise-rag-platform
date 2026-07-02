"""add conversation summaries

Revision ID: 795bc26ab32e
Revises: 9b8880d96422
Create Date: 2026-07-02 09:02:45.862937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "795bc26ab32e"
down_revision: Union[str, Sequence[str], None] = "9b8880d96422"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conversation_summaries",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "conversation_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "summary",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "message_start_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "message_end_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f(
            "ix_conversation_summaries_conversation_id"
        ),
        "conversation_summaries",
        ["conversation_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_conversation_summaries_id"
        ),
        "conversation_summaries",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_conversation_summaries_tenant_id"
        ),
        "conversation_summaries",
        ["tenant_id"],
        unique=False,
    )

    op.add_column(
        "conversations",
        sa.Column(
            "summary",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "conversations",
        sa.Column(
            "message_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.alter_column(
        "conversations",
        "message_count",
        server_default=None,
    )

    op.add_column(
        "conversations",
        sa.Column(
            "last_message_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "conversations",
        sa.Column(
            "conversation_metadata",
            sa.JSON(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "conversations",
        "conversation_metadata",
    )

    op.drop_column(
        "conversations",
        "last_message_at",
    )

    op.drop_column(
        "conversations",
        "message_count",
    )

    op.drop_column(
        "conversations",
        "summary",
    )

    op.drop_index(
        op.f(
            "ix_conversation_summaries_tenant_id"
        ),
        table_name="conversation_summaries",
    )

    op.drop_index(
        op.f(
            "ix_conversation_summaries_id"
        ),
        table_name="conversation_summaries",
    )

    op.drop_index(
        op.f(
            "ix_conversation_summaries_conversation_id"
        ),
        table_name="conversation_summaries",
    )

    op.drop_table(
        "conversation_summaries",
    )