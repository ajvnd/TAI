from sqlalchemy import Column, Integer, String
from src.database import Base


class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
