from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from auth import get_current_user, create_access_token
from crud import create_file
from database import get_db
from schemas import FileResponse
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileResponse)
def upload_file(
    file: UploadFile, 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    # Check if user role is "operator"
    if user.role != "operator":
        raise HTTPException(status_code=403, detail="Only operators can upload files.")

    # Validate file type
    allowed_types = [
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",   # .docx
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",         # .xlsx
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    # Save file to upload directory
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Generate an encrypted URL for the file
    encrypted_url = create_access_token({"file_path": file_path})

    # Save file details to the database
    db_file = create_file(db, file.filename, file_path, user.id, encrypted_url)

    # Return the response
    return FileResponse(
        id=db_file.id,
        name=db_file.name,
        encrypted_url=db_file.encrypted_url
    )
