from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User
from database import get_db

SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": str(data.get("user_id"))})  # Add user_id to 'sub'
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("token",token)
    return token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload",payload)
        return payload
    except JWTError:
        return None



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")  # Extract 'id' from the token
        user_role: str = payload.get("role")  # Extract 'role' from the token

        if not user_id or not user_role:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Convert 'user_id' to integer safely
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID in token")

    # Retrieve the user from the database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
