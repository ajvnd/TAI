from pydantic import BaseModel
from typing import Optional


class SubTaskCreateSchema(BaseModel):
    task_id: int
    title: str
    is_completed: Optional[bool] = None


class SubTaskUpdateSchema(BaseModel):
    task_id: Optional[int] = None
    title: Optional[str] = None
    is_completed: Optional[bool] = None


class SubTaskProgressionSchema(BaseModel):
    progress: Optional[int] = None
