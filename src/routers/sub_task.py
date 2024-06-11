from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import schemas, models, repositories

router = APIRouter()


@router.get("/sub_tasks", status_code=status.HTTP_200_OK)
def get_sub_tasks(db: Session = Depends(models.get_db)):
    return repositories.SubTask(db).get_sub_tasks()


@router.get("/sub_tasks/{sub_task_id}", status_code=status.HTTP_200_OK)
def get_sub_task(sub_task_id: int, response: Response, db: Session = Depends(models.get_db)):
    sub_task = repositories.SubTask(db).get_sub_task(sub_task_id)
    if not sub_task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{sub_task_id} not found"
    return sub_task


@router.post("/sub_tasks", status_code=status.HTTP_201_CREATED)
def create_sub_task(sub_task: schemas.SubTaskCreate, db: Session = Depends(models.get_db)):
    sub_task = models.SubTask(**sub_task.dict())
    repositories.SubTask(db).create_sub_task(sub_task)


@router.put("/sub_tasks/{sub_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_sub_task(sub_task_id: int, sub_task: schemas.SubTaskUpdate, db: Session = Depends(models.get_db)):
    sub_task = models.SubTask(**sub_task.dict())
    sub_task.id = sub_task_id
    repositories.SubTask(db).update_sub_task(sub_task)


@router.put("/sub_tasks/{sub_task_id}/progression", status_code=status.HTTP_204_NO_CONTENT)
def update_sub_task_progression(sub_task_id: int, sub_task_progression: schemas.SubTaskProgression,db: Session = Depends(models.get_db)):
    repositories.SubTask(db).update_sub_task_progression(sub_task_id, sub_task_progression.spend)


@router.delete("/sub_tasks/{sub_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sub_task(sub_task_id: int, response: Response, db: Session = Depends(models.get_db)):
    sub_task = repositories.SubTask(db).get_sub_task(sub_task_id)
    if not sub_task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{sub_task_id} not found"
    repositories.SubTask(db).delete_sub_task(sub_task)
