from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import schemas, models, repositories

router = APIRouter()


@router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks(db: Session = Depends(models.get_db)):
    return repositories.Task(db).get_tasks()


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, response: Response, db: Session = Depends(models.get_db)):
    task = repositories.Task(db).get_task(task_id)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{task_id} not found"
    return task


@router.get("/tasks/{task_id}/sub_tasks", status_code=status.HTTP_200_OK)
def get_sub_tasks(task_id: int, db: Session = Depends(models.get_db)):
    return repositories.SubTask(db).get_sub_tasks(task_id)


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(models.get_db)):
    task = models.Task(**task.dict())
    repositories.Task(db).create_task(task)


@router.post("/tasks/{prompt}", status_code=status.HTTP_201_CREATED)
def create_task(prompt: str, task: schemas.TaskCreate, db: Session = Depends(models.get_db)):

    task = models.Task(**task.dict())
    repositories.Task(db).create_task(task)


@router.put("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(models.get_db)):
    task = models.Task(**task.dict())
    task.id = task_id
    repositories.Task(db).update_task(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, response: Response, db: Session = Depends(models.get_db)):
    task = repositories.Task(db).get_task(task_id)
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{task_id} not found"
    repositories.Task(db).delete_task(task)
