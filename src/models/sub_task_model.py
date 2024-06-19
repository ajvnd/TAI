from datetime import datetime
from faker import Faker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class SubTaskModel(Base):
    __tablename__ = "sub_task"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    title = Column(String(255))
    start_date = Column(DateTime, nullable=False, default=datetime.now())
    pomodoros = Column(Integer, nullable=False)
    progress = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)

    task = relationship('TaskModel', back_populates="sub_tasks")

    @classmethod
    def generate_sub_tasks(cls, count=10):
        fake = Faker()
        sub_tasks = []
        for i in range(count):
            sub_task = SubTaskModel()
            sub_task.task_id = 1
            sub_task.title = fake.word()
            sub_task.start_date = datetime.now()
            sub_task.pomodoros = fake.random_int(1, 20)
            sub_task.duration = sub_task.pomodoros * 25
            sub_task.progress = fake.random_int(0, sub_task.duration)
            sub_task.is_completed = sub_task.progress == sub_task.duration
            sub_task.end_date = datetime.now() if sub_task.is_completed else None
            sub_tasks.append(sub_task)
        return sub_tasks
