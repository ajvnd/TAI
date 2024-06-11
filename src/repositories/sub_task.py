from sqlalchemy.orm import Session, subqueryload
from src import models


class SubTask:
    def __init__(self, db: Session):
        self.db = db

    def get_sub_task(self, sub_task_id: int):
        return self.db.query(models.SubTask).options(subqueryload(models.SubTask.task)).filter(
            models.SubTask.id == sub_task_id).first()

    def get_sub_tasks(self):
        return self.db.query(models.SubTask).all()

    def get_sub_tasks(self, task_id):
        return self.db.query(models.SubTask).filter(models.SubTask.task_id == task_id).all()

    def create_sub_task(self, sub_task: models.SubTask):
        self.db.add(sub_task)
        self.db.commit()

    def update_sub_task(self, sub_task: models.SubTask):
        db_sub_task = self.get_sub_task(sub_task.id)
        for key, value in sub_task.__dict__.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                setattr(db_sub_task, key, value)
        self.db.commit()

    def delete_sub_task(self, sub_task: models.SubTask):
        self.db.delete(sub_task)
        self.db.commit()
