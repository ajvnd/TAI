from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str


class UserCreate(BaseModel):
    title: str


class UserUpdate(BaseModel):
    title: str
