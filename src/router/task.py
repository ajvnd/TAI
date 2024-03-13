from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import schemas, models
from src import repository
from src.database import SessionLocal

task_repository = repository.TaskRepository()

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks(db: Session = Depends(get_db)):
    return task_repository.get_tasks(db)


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, response: Response, db: Session = Depends(get_db)):
    task = task_repository.get_task(task_id, db)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{task_id} not found"
    return task


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    task_repository.create_task(db_task, db)


@router.put("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db_task.id = task_id
    task_repository.update_task(db_task, db)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, response: Response, db: Session = Depends(get_db)):
    task = task_repository.get_task(task_id, db)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{task_id} not found"
    task_repository.delete_task(task, db)
