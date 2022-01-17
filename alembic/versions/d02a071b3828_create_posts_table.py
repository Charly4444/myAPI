"""create posts table

Revision ID: d02a071b3828
Revises: 76cf12c652ef
Create Date: 2022-01-16 13:13:51.149571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd02a071b3828'
down_revision = '76cf12c652ef'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False),
                    sa.Column("content", sa.String(), nullable=False),
                    sa.Column("published", sa.Boolean(), server_default='TRUE', nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"),
                              nullable=False)

                    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
