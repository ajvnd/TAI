from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import models
from src.database import engine
from src.router import task, user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(task.router)
app.include_router(user.router)
models.Base.metadata.create_all(bind=engine)
