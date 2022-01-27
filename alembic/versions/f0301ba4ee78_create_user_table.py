"""Create User, File and UserFiles Tables

Revision ID: f0301ba4ee78
Revises: 
Create Date: 2022-01-25 20:18:49.989403

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database.models.access_rights_enum import AccessRights

# revision identifiers, used by Alembic.
revision = 'f0301ba4ee78'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password', sa.Text, nullable=False),
    )
    op.create_table(
        'file',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('filename', sa.Text, nullable=False),
        sa.Column('filepath', sa.Text, nullable=False),
    )
    op.create_table(
        'user_files',
        sa.Column('user_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('file_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('access_rights', sa.Enum(AccessRights), nullable=False, server_default="VIEWER"),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.ForeignKeyConstraint(['file_id'], ['file.id'])
    )


def downgrade():
    op.drop_table('user_files')
    op.drop_table('file')
    op.drop_table('user')
    op.execute("DROP type accessrights")
