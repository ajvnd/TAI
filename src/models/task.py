from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .base import Base


class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
