from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

from passlib.hash import bcrypt

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hash(user.password)
    new_user = User(
        email=user.email,
        password=hashed_password,
        role=user.role,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
# crud.py
from sqlalchemy.orm import Session
from models import File

def create_file(db: Session, name: str, path: str, uploader_id: int, encrypted_url: str):
    new_file = File(
        name=name,
        path=path,
        uploader_id=uploader_id,
        encrypted_url=encrypted_url
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file
