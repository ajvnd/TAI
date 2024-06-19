from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import schemas, models
from src.repositories import TaskRepository, SubTaskRepository

router = APIRouter()


@router.get("/tasks/{project_id}", status_code=status.HTTP_200_OK)
def get_tasks(project_id, db: Session = Depends(models.get_db)):
    return TaskRepository(db).get_tasks(project_id)


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, response: Response, db: Session = Depends(models.get_db)):
    task = TaskRepository(db).get_task(task_id)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{task_id} not found"
    return task


@router.get("/tasks/{task_id}/sub_tasks", status_code=status.HTTP_200_OK)
def get_sub_tasks(task_id: int, db: Session = Depends(models.get_db)):
    return SubTaskRepository(db).get_sub_tasks(task_id)


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(models.get_db)):
    task = models.TaskModel(**task.dict())
    TaskRepository(db).create_task(task)
    db.commit()
    return task.id


@router.put("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(models.get_db)):
    task = models.TaskModel(**task.dict())
    task.id = task_id
    TaskRepository(db).update_task(task)
    db.commit()


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, response: Response, db: Session = Depends(models.get_db)):
    task = TaskRepository(db).get_task(task_id)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{task_id} not found"
    TaskRepository(db).delete_task(task)
    db.commit()
