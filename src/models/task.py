from faker import Faker
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    title = Column(String(255))
    is_completed = Column(Boolean, default=False)

    project = relationship("Project", back_populates="tasks")
    sub_tasks = relationship('SubTask', back_populates='task')

    @classmethod
    def generate_tasks(cls):
        fake = Faker()

        task = Task()
        task.project_id = 1
        task.title = fake.word()
        task.is_completed = False

        return task
