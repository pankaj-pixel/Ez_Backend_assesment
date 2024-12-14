from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,DateTime
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # 'client' or 'operator'
    is_verified = Column(Boolean, default=False)




class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    encrypted_url = Column(String, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)