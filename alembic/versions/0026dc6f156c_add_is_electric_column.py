# 0026dc6f156c_add_is_electric_column.py

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '0026dc6f156c'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('transport_types', sa.Column('is_electric', sa.Boolean(), nullable=True))

    connection = op.get_bind()
    connection.execute(text('UPDATE transport_types SET is_electric = FALSE WHERE is_electric IS NULL'))

    op.alter_column('transport_types', 'is_electric', nullable=False)

def downgrade():
    op.drop_column('transport_types', 'is_electric')
