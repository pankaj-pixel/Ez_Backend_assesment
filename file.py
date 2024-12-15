from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from auth import get_current_user, create_access_token
from crud import create_file_record
from database import get_db
from schemas import FileResponse
import os
from models import File 
from auth import SECRET_KEY
# Define the directory where uploaded files will be stored
UPLOAD_DIR = "uploads"

# Ensure the directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

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
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",  
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",   
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",         
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    # Save file to the upload directory
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Generate an encrypted URL for the file
    encrypted_url = create_access_token({"file_path": file_path})

    # Save file details to the database
    db_file = create_file_record(
        db=db,
        filename=file.filename,
        file_path=file_path,
        uploaded_by=user.id,
        encrypted_url=encrypted_url
    )

    # Return the response
    return FileResponse(
        id=db_file.id,
        filename=db_file.filename,
        encrypted_url=db_file.encrypted_url
    )


@router.get("/allfiles", response_model=list[str])  # response model as a list of strings (filenames)
def get_all_files(db: Session = Depends(get_db)):
    # Query all files and only select the filename column
    files = db.query(File.filename).all()
    
    if not files:
        raise HTTPException(status_code=404, detail="No files found.")
    
    # Extracting the filenames from the query result
    filenames = [file.filename for file in files]
    
    # Return the list of filenames
    return filenames




@router.get("/download-file/{file_id}", response_model=dict)
def download_file(file_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Ensure the user is a client
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Access denied. Only clients can download files.")
    
    # Get the file record by ID
    file = db.query(File).filter(File.id == file_id).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found.")
    
    # Generate a secure download link (encrypted URL)
    encrypted_url = create_access_token({"file_id": file.id})
    
    # Return the download link
    return {
        "download-link": f"/download-fle/{encrypted_url}", 
        "message": "success"
    }



