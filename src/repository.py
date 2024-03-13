from sqlalchemy.orm import Session

from src import models


class TaskRepository:
    def get_task(self, task_id: int, db: Session):
        return db.query(models.Task).filter(models.Task.id == task_id).first()

    def get_tasks(self, db: Session):
        return db.query(models.Task).all()

    def create_task(self, db_task: models.Task, db: Session):
        db.add(db_task)
        db.commit()

    def update_task(self, db_task: models.Task, db: Session):
        task = db.query(models.Task).filter(models.Task.id == db_task.id).first()
        task.title = db_task.title
        db.commit()

    def delete_task(self, db_task: models.Task, db: Session):
        db.delete(db_task)
        db.commit()
