from pydantic import BaseModel


class ProjectCreateSchema(BaseModel):
    title: str


class ProjectUpdateSchema(BaseModel):
    title: str
