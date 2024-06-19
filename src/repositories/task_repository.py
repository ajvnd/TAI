from sqlalchemy.orm import Session, subqueryload
from src.models import TaskModel


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: int):
        return self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

    def get_tasks(self):
        return self.db.query(TaskModel).all()

    def get_tasks(self, project_id: int):
        return self.db.query(TaskModel).filter(TaskModel.project_id == project_id).all()

    def create_task(self, task: TaskModel):
        self.db.add(task)

    def update_task(self, task: TaskModel):
        db_task = self.get_task(task.id)
        for key, value in task.__dict__.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                setattr(db_task, key, value)

    def delete_task(self, task: TaskModel):
        self.db.delete(task)
