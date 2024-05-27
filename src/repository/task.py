from sqlalchemy.orm import Session
from src.models import TaskModel

task_model = TaskModel


class Task:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: int):
        return self.db.query(task_model).filter(task_model.id == task_id).first()

    def get_tasks(self):
        return self.db.query(task_model).all()

    def create_task(self, db_task: task_model):
        self.db.add(db_task)
        self.db.commit()

    def update_task(self, db_task: task_model):
        task = self.db.query(task_model).filter(task_model.id == db_task.id).first()
        for key, value in db_task.__dict__.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                setattr(task, key, value)
        self.db.commit()

    def delete_task(self, db_task: task_model):
        self.db.delete(db_task)
        self.db.commit()
