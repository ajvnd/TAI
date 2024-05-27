from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import schemas
from src.models import get_db, TaskModel
from src.repository import TaskRepository

task_model = TaskModel

router = APIRouter()


def get_task_repository(db: Session = Depends(get_db)):
    return TaskRepository(db)


@router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks(db: Session = Depends(get_db)):
    return get_task_repository(db).get_tasks()


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, response: Response, db: Session = Depends(get_db)):
    task = get_task_repository(db).get_task(task_id)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{task_id} not found"
    return task


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = task_model(**task.dict())
    get_task_repository(db).create_task(db_task)


@router.put("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = task_model(**task.dict())
    db_task.id = task_id
    get_task_repository(db).update_task(db_task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, response: Response, db: Session = Depends(get_db)):
    task = get_task_repository(db).get_task(task_id)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{task_id} not found"
    get_task_repository(db).delete_task(task)
