from faker import Faker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class SubTask(Base):
    __tablename__ = "sub_task"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    title = Column(String(255))
    is_completed = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=True)

    task = relationship('Task', back_populates="sub_tasks")

    @classmethod
    def generate_sub_tasks(cls, count=10):
        fake = Faker()
        sub_tasks = []
        for i in range(count):
            sub_task = SubTask()
            sub_task.task_id = 1
            sub_task.title = fake.word()
            sub_task.start_date = fake.date_between(start_date=datetime.date(2024, 6, 1),
                                                    end_date=datetime.date(2024, 6, 10))
            sub_task.due_date = fake.date_between(start_date="today", end_date=datetime.date(2025, 6, 1))
            sub_task.is_completed = sub_task.due_date < datetime.date.today()
            sub_tasks.append(sub_task)
        return sub_tasks
