from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserLogin
from crud import create_user, get_user_by_email
from auth import create_access_token
from passlib.hash import bcrypt

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Validate role
    if user.role not in ["operator", "client"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    # Check if user exists
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    new_user = create_user(db, user)
    return {"message": "User created successfully", "user": new_user}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not bcrypt.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"id": db_user.id, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-email/{email}")
def verify_email(email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}
