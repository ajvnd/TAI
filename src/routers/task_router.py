from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src.repositories import TaskRepository, SubTaskRepository
from src.models import TaskModel, get_db
from src.schemas.task_schema import TaskCreateSchema, TaskUpdateSchema

router = APIRouter()


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, response: Response, db: Session = Depends(get_db)):
    task = TaskRepository(db).get_task(task_id)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
    return task


@router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks(project_id, db: Session = Depends(get_db)):
    return TaskRepository(db).get_tasks()


@router.get("/tasks/{task_id}/sub_tasks", status_code=status.HTTP_200_OK)
def get_sub_tasks(task_id: int, db: Session = Depends(get_db)):
    return SubTaskRepository(db).get_sub_tasks(task_id)


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_create_schema: TaskCreateSchema, db: Session = Depends(get_db)):
    task_create_schema = TaskModel(**task_create_schema.dict())
    TaskRepository(db).create_task(task_create_schema)
    db.commit()
    return task_create_schema.id


@router.put("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(task_id: int, task_update_schema: TaskUpdateSchema, db: Session = Depends(get_db)):
    task_update_schema = TaskModel(**task_update_schema.dict())
    task_update_schema.id = task_id
    TaskRepository(db).update_task(task_update_schema)
    db.commit()


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, response: Response, db: Session = Depends(get_db)):
    task = TaskRepository(db).get_task(task_id)

    # make sure the task exists before deleting it
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND

    TaskRepository(db).delete_task(task)
    db.commit()
