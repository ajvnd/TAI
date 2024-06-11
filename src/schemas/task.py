from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    is_completed: Optional[bool] = None


class TaskUpdate(BaseModel):
    id: Optional[int]
    title: Optional[str] = None
    is_completed: Optional[bool] = None
