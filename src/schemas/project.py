from pydantic import BaseModel
from typing import Optional


class ProjectCreate(BaseModel):
    title: str


class ProjectUpdate(BaseModel):
    task_id: Optional[int]
