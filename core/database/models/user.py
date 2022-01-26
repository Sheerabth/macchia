from core.database.models.base import Base

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4


class User(Base):
    __tablename__ = 'User'

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    Username = Column(String)
    Password = Column(Text)

    files = relationship("UserFilesAssociation", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.ID}, name={self.Username}, files = {self.files})>"
