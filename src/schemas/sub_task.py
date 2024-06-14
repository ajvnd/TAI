from pydantic import BaseModel
from typing import Optional


class SubTaskCreate(BaseModel):
    task_id: Optional[int]
    title: str
    is_completed: Optional[bool] = None
    progress: Optional[int] = None
    duration: Optional[int] = None


class SubTaskUpdate(BaseModel):
    task_id: Optional[int]
    title: Optional[str] = None
    is_completed: Optional[bool] = None
    progress: Optional[int] = None
    duration: Optional[int] = None


class SubTaskProgression(BaseModel):
    progress: Optional[int] = None
