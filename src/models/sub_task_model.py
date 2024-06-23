from datetime import datetime
from faker import Faker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .app_model import AppModel


class SubTaskModel(Base):
    __tablename__ = "sub_task"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    title = Column(String(255))
    start_date = Column(DateTime, nullable=True)
    progress = Column(Integer, nullable=True)
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
            sub_task.is_completed = sub_task.progress == AppModel.default_pomodoro_time
            sub_task.progress = fake.random_int(1, 24)
            # start date has value if progress greater 0, meaning the user hit the progression button
            sub_task.start_date = datetime.now() if sub_task.progress > 0 else None
            # end date has value if task is completed
            sub_task.end_date = datetime.now() if sub_task.is_completed else None
            sub_tasks.append(sub_task)
        return sub_tasks
