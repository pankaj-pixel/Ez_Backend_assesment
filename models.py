from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # 'client' or 'operator'
    is_verified = Column(Boolean, default=False)

    
    files = relationship("File", back_populates="uploader", cascade="all, delete-orphan")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True ,autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    encrypted_url = Column(String(255), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)

   
    uploader = relationship("User", back_populates="files")
