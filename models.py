from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ensure autoincrement
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(String(10), nullable=False)  # 'ops' or 'client'
    is_verified = Column(Boolean, default=False)
    # Relationship with Fi
    files = relationship("File", back_populates="uploader")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    encrypted_url = Column(String(500), nullable=False)

    uploader = relationship("User", back_populates="files")
