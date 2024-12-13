from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FileUpload(BaseModel):
    filename: str
    encrypted_url: str

class FileResponse(BaseModel):
    filename: str
    encrypted_url: str
