from fastapi import FastAPI
from database import Base, engine
import user
import file

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user.router, prefix="/auth", tags=["User Management"])
app.include_router(file.router, prefix="/file", tags=["File Management"])