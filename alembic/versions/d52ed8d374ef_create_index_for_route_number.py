from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd52ed8d374ef'  
down_revision = '0026dc6f156c'  
branch_labels = None
depends_on = None

def upgrade():
    
    op.create_index('ix_route_number', 'routes', ['route_number'])

def downgrade():
    
    op.drop_index('ix_route_number', table_name='routes')
