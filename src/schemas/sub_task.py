from pydantic import BaseModel
from typing import Optional


class SubTaskCreate(BaseModel):
    task_id: Optional[int]
    title: str
    pomodoros: Optional[int] = None
    progress: Optional[int] = None
    is_completed: Optional[bool] = None


class SubTaskUpdate(BaseModel):
    task_id: Optional[int]
    title: Optional[str] = None
    pomodoros: Optional[int] = None
    progress: Optional[int] = None
    is_completed: Optional[bool] = None


class SubTaskProgression(BaseModel):
    progress: Optional[int] = None
