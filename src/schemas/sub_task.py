from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubTaskCreate(BaseModel):
    task_id: Optional[int]
    title: str
    is_completed: Optional[bool] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None


class SubTaskUpdate(BaseModel):
    task_id: Optional[int]
    title: Optional[str] = None
    is_completed: Optional[bool] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
