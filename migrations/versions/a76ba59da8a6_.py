"""empty message

Revision ID: a76ba59da8a6
Revises: da10a0744947
Create Date: 2023-12-20 22:15:06.372971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a76ba59da8a6'
down_revision = 'da10a0744947'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_on', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('changed_on', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('stock_type', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('stock_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('purchase_price', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('sale_price', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('created_by_fk', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('changed_by_fk', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'ab_user', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'ab_user', ['changed_by_fk'], ['id'])
        batch_op.create_foreign_key(None, 'ab_user', ['created_by_fk'], ['id'])
        batch_op.drop_column('name')

    with op.batch_alter_table('stock', schema=None) as batch_op:
        batch_op.alter_column('quantity',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('purchase_price',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'ab_user', ['user_id'], ['id'])
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('purchase_price',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('quantity',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('changed_by_fk')
        batch_op.drop_column('created_by_fk')
        batch_op.drop_column('sale_price')
        batch_op.drop_column('purchase_price')
        batch_op.drop_column('quantity')
        batch_op.drop_column('stock_id')
        batch_op.drop_column('stock_type')
        batch_op.drop_column('user_id')
        batch_op.drop_column('changed_on')
        batch_op.drop_column('created_on')

    # ### end Alembic commands ###