"""create vote table

Revision ID: a5b7b2525151
Revises: d02a071b3828
Create Date: 2022-01-16 13:20:53.748505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5b7b2525151'
down_revision = 'd02a071b3828'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("votes", sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"),
                                       primary_key=True),
                    sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"),
                              primary_key=True),
                    )
    pass


def downgrade():
    op.drop_table("votes")
    pass
