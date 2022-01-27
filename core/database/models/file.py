from core.database.models.base import Base

from sqlalchemy import Column, Text, BIGINT
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4


class File(Base):
    __tablename__ = 'file'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    filename = Column(Text)
    filepath = Column(Text)
    file_size = Column(BIGINT)
    created_time = Column(TIMESTAMP)

    users = relationship("UserFilesAssociation", back_populates="file")

    def __repr__(self):
        return f"<File(id={self.id}, filename={self.filename}, filepath={self.filepath}, users={self.users})>"
