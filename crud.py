from sqlalchemy.orm import Session
from models import User,File
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

def create_file_record(db: Session, filename: str, file_path: str, uploaded_by: int, encrypted_url: str):
    new_file = File(
        filename=filename,
        file_path=file_path,
        uploaded_by=uploaded_by,
        encrypted_url=encrypted_url
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file
