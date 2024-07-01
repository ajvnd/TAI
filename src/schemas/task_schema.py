from pydantic import BaseModel
from typing import Optional


class TaskCreateSchema(BaseModel):
    project_id: int
    title: str
    done: Optional[bool] = None


class TaskUpdateSchema(BaseModel):
    project_id: int
    title: Optional[str] = None
    done: Optional[bool] = None
