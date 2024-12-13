from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from crud import create_file, get_all_files
from database import get_db
from security import create_access_token

router = APIRouter()

@router.post("/upload")
def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    if file.content_type not in [
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    encrypted_url = create_access_token({"path": file_path})
    create_file(db, file.filename, file_path, uploader_id=1, encrypted_url=encrypted_url)  # Replace `uploader_id` with dynamic value
    return {"message": "File uploaded successfully", "encrypted_url": encrypted_url}
