from fastapi import FastAPI
import auth, file
from database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(auth.router, prefix="/auth")
app.include_router(file.router, prefix="/file")
