"""create user table

Revision ID: 7d7d1a6aa2cb
Revises: 
Create Date: 2022-12-03 17:34:07.744442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d7d1a6aa2cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("email", sa.String, nullable=False, unique=True),
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
