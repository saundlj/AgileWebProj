"""empty message

Revision ID: 3022c3c5c33a
Revises: 113b8da23865
Create Date: 2024-05-07 14:34:44.009168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3022c3c5c33a'
down_revision = '113b8da23865'
branch_labels = None
depends_on = None

def upgrade():
    # Add the new column 'salary' to the 'Posts' table
    op.add_column('Post', sa.Column('salary', sa.Float, nullable=True))

def downgrade():
    # Remove the 'salary' column from the 'Posts' table (if needed)
    op.drop_column('Post', 'salary')
