from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import ProjectModel, TaskModel, SubTaskModel, SessionLocal, Base, engine
from src.routers import project_router, task_router, sub_task_router

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

# Include endpoints in the main application
app.include_router(project_router)
app.include_router(task_router)
app.include_router(sub_task_router)

db = SessionLocal()
try:
    if db.query(ProjectModel).count() == 0:
        db.add(ProjectModel.generate_projects())
        db.commit()

    if db.query(TaskModel).count() == 0:
        db.add(TaskModel.generate_tasks())
        db.commit()

    if db.query(SubTaskModel).count() == 0:
        db.bulk_save_objects(SubTaskModel.generate_sub_tasks())
        db.commit()
finally:
    db.close()
