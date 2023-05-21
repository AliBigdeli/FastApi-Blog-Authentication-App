"""empty message

Revision ID: f7b773c328b2
Revises: dda127c2c99d
Create Date: 2023-05-01 03:31:44.615787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f7b773c328b2"
down_revision = "dda127c2c99d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "is_published")
    op.drop_column("posts", "modified_at")
    op.drop_column("posts", "created_at")
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "modified_at",
            sa.DateTime(),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "is_published",
            sa.Boolean(),
            nullable=True,
            server_default=sa.false(),
        ),
    )
    op.execute("UPDATE posts SET created_at = NOW() WHERE created_at IS NULL")
    op.execute(
        "UPDATE posts SET is_published = true WHERE is_published IS NULL"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
