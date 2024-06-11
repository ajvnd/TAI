from sqlalchemy.orm import Session, subqueryload
from src import models


class Task:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: int):
        return self.db.query(models.Task).filter(models.Task.id == task_id).first()

    def get_tasks(self):
        return self.db.query(models.Task).all()

    def create_task(self, task: models.Task):
        self.db.add(task)
        self.db.commit()

    def update_task(self, task: models.Task):
        db_task = self.get_task(task.id)
        for key, value in task.__dict__.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                setattr(db_task, key, value)
        self.db.commit()

    def delete_task(self, task: models.Task):
        self.db.delete(task)
        self.db.commit()
