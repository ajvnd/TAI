from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    project_id: int
    title: str
    is_completed: Optional[bool] = None


class TaskUpdate(BaseModel):
    project_id: int
    title: Optional[str] = None
    is_completed: Optional[bool] = None
