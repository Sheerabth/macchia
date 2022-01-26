from core.database.models.base import Base

from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4


class File(Base):
    __tablename__ = 'File'

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    Filename = Column(Text)
    Filepath = Column(Text)

    users = relationship("UserFilesAssociation", back_populates="file")

    def __repr__(self):
        return f"<File(id={self.ID}, filename={self.Filename})>"
