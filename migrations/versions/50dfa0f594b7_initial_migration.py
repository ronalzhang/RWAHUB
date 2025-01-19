"""initial migration

Revision ID: 50dfa0f594b7
Revises: 
Create Date: 2025-01-18 03:14:30.100800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50dfa0f594b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('asset_type', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=200), nullable=False),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('total_value', sa.Float(), nullable=True),
    sa.Column('token_symbol', sa.String(length=20), nullable=False),
    sa.Column('token_price', sa.Float(), nullable=False),
    sa.Column('token_supply', sa.Integer(), nullable=True),
    sa.Column('token_address', sa.String(length=42), nullable=True),
    sa.Column('annual_revenue', sa.Float(), nullable=False),
    sa.Column('images', sa.Text(), nullable=True),
    sa.Column('documents', sa.Text(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('reject_reason', sa.String(length=200), nullable=True),
    sa.Column('owner_address', sa.String(length=42), nullable=False),
    sa.Column('creator_address', sa.String(length=42), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_by', sa.String(length=42), nullable=True),
    sa.CheckConstraint('annual_revenue > 0', name='ck_annual_revenue_positive'),
    sa.CheckConstraint('area > 0', name='ck_area_positive'),
    sa.CheckConstraint('status IN (1, 2, 3, 4)', name='ck_status_valid'),
    sa.CheckConstraint('token_price > 0', name='ck_token_price_positive'),
    sa.CheckConstraint('token_supply > 0', name='ck_token_supply_positive'),
    sa.CheckConstraint('total_value > 0', name='ck_total_value_positive'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token_address'),
    sa.UniqueConstraint('token_symbol')
    )
    with op.batch_alter_table('assets', schema=None) as batch_op:
        batch_op.create_index('ix_assets_asset_type', ['asset_type'], unique=False)
        batch_op.create_index('ix_assets_created_at', ['created_at'], unique=False)
        batch_op.create_index('ix_assets_location', ['location'], unique=False)
        batch_op.create_index('ix_assets_name', ['name'], unique=False)
        batch_op.create_index('ix_assets_status', ['status'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('eth_address', sa.String(length=42), nullable=True),
    sa.Column('nonce', sa.String(length=100), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('settings', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('eth_address'),
    sa.UniqueConstraint('username')
    )
    op.create_table('dividend_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False, comment='总分红金额(包含所有费用)'),
    sa.Column('actual_amount', sa.Float(), nullable=False, comment='实际分配金额'),
    sa.Column('platform_fee', sa.Float(), nullable=False, comment='平台费用'),
    sa.Column('holders_count', sa.Integer(), nullable=False, comment='持有人数'),
    sa.Column('gas_used', sa.Integer(), nullable=False, comment='gas消耗'),
    sa.Column('tx_hash', sa.String(length=66), nullable=False, comment='交易哈希'),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('actual_amount = total_amount - platform_fee', name='ck_actual_amount'),
    sa.CheckConstraint('platform_fee = total_amount * 0.015', name='ck_platform_fee_rate'),
    sa.CheckConstraint('total_amount >= 10000', name='ck_total_amount_min'),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tx_hash')
    )
    with op.batch_alter_table('dividend_records', schema=None) as batch_op:
        batch_op.create_index('ix_dividend_records_asset_id', ['asset_id'], unique=False)
        batch_op.create_index('ix_dividend_records_created_at', ['created_at'], unique=False)

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
    with op.batch_alter_table('dividend_records', schema=None) as batch_op:
        batch_op.drop_index('ix_dividend_records_created_at')
        batch_op.drop_index('ix_dividend_records_asset_id')

    op.drop_table('dividend_records')
    op.drop_table('users')
    with op.batch_alter_table('assets', schema=None) as batch_op:
        batch_op.drop_index('ix_assets_status')
        batch_op.drop_index('ix_assets_name')
        batch_op.drop_index('ix_assets_location')
        batch_op.drop_index('ix_assets_created_at')
        batch_op.drop_index('ix_assets_asset_type')

    op.drop_table('assets')
    # ### end Alembic commands ###
