"""Create User Table

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
        'User',
        sa.Column('ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('Username', sa.String(50), nullable=False),
        sa.Column('Password', sa.String(50), nullable=False),
    )
    op.create_table(
        'File',
        sa.Column('ID', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('Filename', sa.Text, nullable=False),
        sa.Column('Filepath', sa.Text, nullable=False),
    )
    op.create_table(
        'UserFiles',
        sa.Column('UserId', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('FileId', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('AccessRights', sa.Enum(AccessRights), nullable=False, server_default="VIEWER"),
        sa.ForeignKeyConstraint(['UserId'], ['User.ID']),
        sa.ForeignKeyConstraint(['FileId'], ['File.ID'])
    )


def downgrade():
    op.drop_table('UserFiles')
    op.drop_table('File')
    op.drop_table('User')
