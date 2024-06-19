from pydantic import BaseModel
from typing import Optional


class SubTaskCreateSchema(BaseModel):
    task_id: Optional[int]
    title: str
    pomodoros: Optional[int] = None
    progress: Optional[int] = None
    is_completed: Optional[bool] = None


class SubTaskUpdateSchema(BaseModel):
    task_id: Optional[int]
    title: Optional[str] = None
    pomodoros: Optional[int] = None
    progress: Optional[int] = None
    is_completed: Optional[bool] = None


class SubTaskProgressionSchema(BaseModel):
    progress: Optional[int] = None
