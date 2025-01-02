"""add specifications column to transport_types

Revision ID: 710e6b9ce181
Revises: d52ed8d374ef
Create Date: 2025-01-02 20:53:47.492743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql  

# revision identifiers, used by Alembic.
revision: str = '710e6b9ce181'
down_revision: Union[str, None] = 'd52ed8d374ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")  
    op.add_column('transport_types', sa.Column('specifications', postgresql.JSONB(), nullable=True))  
    op.execute("CREATE INDEX IF NOT EXISTS ix_specifications_gin ON transport_types USING gin(specifications jsonb_ops)")  


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_specifications_gin")  
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")  
    op.drop_column('transport_types', 'specifications')  
