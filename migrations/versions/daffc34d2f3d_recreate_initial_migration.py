"""recreate initial migration

Revision ID: daffc34d2f3d
Revises: 
Create Date: 2025-01-19 15:17:17.323740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daffc34d2f3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('asset_type', sa.Enum('REAL_ESTATE', 'SEMI_REAL_ESTATE', name='assettype'), nullable=False),
    sa.Column('token_code', sa.String(length=10), nullable=False),
    sa.Column('token_symbol', sa.String(length=20), nullable=False),
    sa.Column('token_price', sa.Float(), nullable=False),
    sa.Column('token_supply', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=200), nullable=False),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('total_value', sa.Float(), nullable=True),
    sa.Column('annual_revenue', sa.Float(), nullable=False),
    sa.Column('images', sa.Text(), nullable=True),
    sa.Column('documents', sa.Text(), nullable=True),
    sa.Column('owner_address', sa.String(length=42), nullable=False),
    sa.Column('token_address', sa.String(length=42), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'DELETED', name='assetstatus'), nullable=False),
    sa.Column('reject_reason', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('eth_address', sa.String(length=42), nullable=True),
    sa.Column('nonce', sa.String(length=100), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('eth_address'),
    sa.UniqueConstraint('username')
    )
    op.create_table('trades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('trader_address', sa.String(length=42), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_self_trade', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trades')
    op.drop_table('users')
    op.drop_table('assets')
    # ### end Alembic commands ###
