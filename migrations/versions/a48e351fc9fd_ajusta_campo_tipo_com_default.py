"""ajusta campo tipo com default

Revision ID: a48e351fc9fd
Revises: 38aefaa38f5c
Create Date: 2026-02-05 01:04:12.851491

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a48e351fc9fd'
down_revision = '38aefaa38f5c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('tipo', sa.String(length=20), nullable=False, server_default='aluno')
        )


def downgrade():
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('tipo')


    op.create_table('feedback',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('comentario', mysql.VARCHAR(length=300), nullable=False),
    sa.Column('nota', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('usuario_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('refeicao_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['refeicao_id'], ['refeicao.id'], name=op.f('feedback_ibfk_1')),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name=op.f('feedback_ibfk_2')),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('refeicao',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
