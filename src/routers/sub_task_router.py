from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src.models import SubTaskModel, get_db
from src.repositories import SubTaskRepository
from src.schemas.sub_task_schema import SubTaskCreateSchema, SubTaskUpdateSchema, SubTaskProgressionSchema

router = APIRouter()


@router.get("/sub_tasks", status_code=status.HTTP_200_OK)
def get_sub_tasks(db: Session = Depends(get_db)):
    return SubTaskRepository(db).get_sub_tasks()


@router.get("/sub_tasks/{sub_task_id}", status_code=status.HTTP_200_OK)
def get_sub_task(sub_task_id: int, response: Response, db: Session = Depends(get_db)):
    sub_task = SubTaskRepository(db).get_sub_task(sub_task_id)
    if not sub_task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{sub_task_id} not found"
    return sub_task


@router.post("/sub_tasks", status_code=status.HTTP_201_CREATED)
def create_sub_task(sub_task_create_schema: SubTaskCreateSchema, db: Session = Depends(get_db)):
    sub_task_create_schema = SubTaskModel(**sub_task_create_schema.dict())
    SubTaskRepository(db).create_sub_task(sub_task_create_schema)
    db.commit()
    return sub_task_create_schema.id


@router.put("/sub_tasks/{sub_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_sub_task(sub_task_id: int, sub_task_update_schema: SubTaskUpdateSchema, db: Session = Depends(get_db)):
    sub_task_update_schema = SubTaskModel(**sub_task_update_schema.dict())
    sub_task_update_schema.id = sub_task_id
    SubTaskRepository(db).update_sub_task(sub_task_update_schema)
    db.commit()


@router.put("/sub_tasks/{sub_task_id}/progression", status_code=status.HTTP_204_NO_CONTENT)
def update_sub_task_progression(sub_task_id: int, sub_task_progression_schema: SubTaskProgressionSchema,
                                db: Session = Depends(get_db)):
    # TODO: if the progress is zero, set start_date as of now
    SubTaskRepository(db).update_sub_task_progression(sub_task_id, sub_task_progression_schema.progress)
    db.commit()


@router.delete("/sub_tasks/{sub_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sub_task(sub_task_id: int, response: Response, db: Session = Depends(get_db)):
    sub_task = SubTaskRepository(db).get_sub_task(sub_task_id)
    if not sub_task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{sub_task_id} not found"
    SubTaskRepository(db).delete_sub_task(sub_task)
    db.commit()
