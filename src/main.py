from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router import user, task
from src.models import Base, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables if they don't already exist.
Base.metadata.create_all(bind=engine)

# Include task endpoints in the main application
app.include_router(task.router)

# Include user endpoints in the application
app.include_router(user.router)
