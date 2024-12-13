from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserSignup, UserLogin
from crud import create_user, get_user_by_email
from security import verify_password, create_access_token
from database import get_db

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(db, user.email, user.password, role="client")
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserSignup, UserLogin
from crud import create_user, get_user_by_email
from security import verify_password, create_access_token
from database import get_db

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(db, user.email, user.password, role="client")
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}
