from pydantic import BaseModel
from typing import Optional


class SubTaskCreateSchema(BaseModel):
    task_id: int
    title: str
    pomodoros: int
    is_completed: Optional[bool] = None


class SubTaskUpdateSchema(BaseModel):
    task_id: Optional[int] = None
    title: Optional[str] = None
    pomodoros: Optional[int] = None
    is_completed: Optional[bool] = None


class SubTaskProgressionSchema(BaseModel):
    progress: Optional[int] = None
