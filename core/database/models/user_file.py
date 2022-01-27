from core.database.models.base import Base

from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.orm import relationship

from core.database.models.access_rights_enum import AccessRights


class UserFilesAssociation(Base):
    __tablename__ = 'user_files'

    user_id = Column(ForeignKey('user.id'), primary_key=True)
    file_id = Column(ForeignKey('file.id'), primary_key=True)
    access_rights = Column(Enum(AccessRights), nullable=False, default=AccessRights.VIEWER)

    user = relationship("User", back_populates="files")
    file = relationship("File", back_populates="users")

    def __repr__(self):
        return f"<UserFile(UserId={self.user_id}, FileId={self.file_id}, AccessRights={self.access_rights})>"
