from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
