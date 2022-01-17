"""remove owner_id as unique

Revision ID: 92c893e7535c
Revises: ead2ad297243
Create Date: 2022-01-16 16:03:56.908884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92c893e7535c'
down_revision = 'ead2ad297243'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("posts", "owner_id")
    op.add_column("posts", sa.Column("owner_id", sa.Integer(),
                                     sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True))
    pass


def downgrade():
    pass
