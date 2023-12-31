"""db.Date

Revision ID: 5cd8d55bbed7
Revises: 5e241139ed15
Create Date: 2023-12-02 19:19:12.235369

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5cd8d55bbed7'
down_revision = '5e241139ed15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('fecha_nacimiento',
               existing_type=mysql.VARCHAR(length=15),
               type_=sa.Date(),
               existing_nullable=False)
        batch_op.alter_column('localidad',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('localidad',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('fecha_nacimiento',
               existing_type=sa.Date(),
               type_=mysql.VARCHAR(length=15),
               existing_nullable=False)

    # ### end Alembic commands ###
