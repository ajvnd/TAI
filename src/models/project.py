from faker import Faker
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))

    tasks = relationship('Task', back_populates='project')

    @classmethod
    def generate_projects(cls):
        fake = Faker()

        task = Project()
        task.title = fake.word()

        return task
