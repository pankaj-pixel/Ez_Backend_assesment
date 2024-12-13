from sqlalchemy.orm import Session
from models import User, File
from security import hash_password

# User CRUD
def create_user(db: Session, email: str, password: str, role: str):
    hashed_password = hash_password(password)
    db_user = User(email=email, password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# File CRUD
def create_file(db: Session, filename: str, file_path: str, uploader_id: int, encrypted_url: str):
    db_file = File(filename=filename, file_path=file_path, uploaded_by=uploader_id, encrypted_url=encrypted_url)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_all_files(db: Session):
    return db.query(File).all()
