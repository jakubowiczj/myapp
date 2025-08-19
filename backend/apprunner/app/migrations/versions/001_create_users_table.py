from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_create_users_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create ENUM type
    user_status_enum = postgresql.ENUM('active', 'inactive', name='user_status')
    user_status_enum.create(op.get_bind())

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('first_name', sa.String(length=80), nullable=False),
        sa.Column('last_name', sa.String(length=120), nullable=False),
        sa.Column('city', sa.String(length=120), nullable=True),
        sa.Column('work_location', sa.String(length=120), nullable=True),
        sa.Column('status', user_status_enum, nullable=False, server_default='active'),
        sa.Column('avatar_url', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Create indexes
    op.create_index('idx_last_name', 'users', ['last_name'])
    op.create_index('idx_city_status', 'users', ['city', 'status'])

def downgrade():
    # Drop indexes
    op.drop_index('idx_city_status', 'users')
    op.drop_index('idx_last_name', 'users')

    # Drop users table
    op.drop_table('users')

    # Drop ENUM type
    user_status_enum = postgresql.ENUM(name='user_status')
    user_status_enum.drop(op.get_bind())
