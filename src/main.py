from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import models, routers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables if they don't already exist.
models.Base.metadata.create_all(bind=models.engine)

# Include endpoints in the main application
app.include_router(routers.task.router)
app.include_router(routers.sub_task.router)

db = models.SessionLocal()
try:
    db.add(models.Project.generate_projects())

    db.add(models.Task.generate_tasks())
    db.commit()

    db.bulk_save_objects(models.SubTask.generate_sub_tasks())
    db.commit()
finally:
    db.close()
