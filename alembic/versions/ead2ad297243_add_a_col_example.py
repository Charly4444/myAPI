"""add a col Example

Revision ID: ead2ad297243
Revises: a5b7b2525151
Create Date: 2022-01-16 13:28:01.276797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ead2ad297243'
down_revision = 'a5b7b2525151'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("hours", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "hours")
    pass
