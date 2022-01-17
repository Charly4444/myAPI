"""create users table

Revision ID: 76cf12c652ef
Revises: 
Create Date: 2022-01-16 13:08:37.783567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76cf12c652ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("email", sa.String(), nullable=False, unique=True),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
