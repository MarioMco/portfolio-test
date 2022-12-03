"""add users rest of columns

Revision ID: de23b06aab37
Revises: 7d7d1a6aa2cb
Create Date: 2022-12-03 17:44:17.356182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de23b06aab37'
down_revision = '7d7d1a6aa2cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users",sa.Column("password", sa.String(), nullable=False))
    op.add_column("users",sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))
    
    pass


def downgrade() -> None:
    op.drop_column("users", "password")
    op.drop_column("users", "created_at")
    pass
