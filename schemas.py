from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_verified: bool




class FileResponse(BaseModel):
    id: int
    filename: str
    encrypted_url: str

    class Config:
        orm_mode = True
