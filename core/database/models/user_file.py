from core.database.models.base import Base

from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.orm import relationship

from uuid import uuid4
from core.database.models.access_rights_enum import AccessRights

class UserFilesAssociation(Base):
    __tablename__ = 'UserFiles'

    UserId = Column(ForeignKey('User.ID'), primary_key=True, default=uuid4)
    FileId = Column(ForeignKey('File.ID'), primary_key=True, default=uuid4)
    AccessRights = Column(Enum(AccessRights), nullable=False, default=AccessRights.VIEWER)

    user = relationship("User", back_populates="files")
    file = relationship("File", back_populates="users")

    def __repr__(self):
        return f"<UserFile(UserId={self.UserId}, FileId={self.FileId}, AccessRights={self.AccessRights})>"
