from faker import Faker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class SubTaskModel(Base):
    __tablename__ = "sub_task"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    title = Column(String(255))
    is_completed = Column(Boolean, default=False)
    progress = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)

    task = relationship('TaskModel', back_populates="sub_tasks")

    @classmethod
    def generate_sub_tasks(cls, count=10):
        fake = Faker()
        sub_tasks = []
        for i in range(count):
            sub_task = SubTaskModel()
            sub_task.task_id = 1
            sub_task.title = fake.word()
            sub_task.duration = fake.random_int(0, 1440)
            sub_task.progress = fake.random_int(0, sub_task.duration)
            sub_task.is_completed = sub_task.progress == sub_task.duration
            sub_tasks.append(sub_task)
        return sub_tasks
