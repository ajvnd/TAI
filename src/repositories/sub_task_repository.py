from sqlalchemy.orm import Session, subqueryload
from src.models import SubTaskModel, AppModel
from datetime import datetime


class SubTaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_sub_task(self, sub_task_id: int) -> SubTaskModel:
        return (self.db.query(SubTaskModel)
                .options(subqueryload(SubTaskModel.task))
                .filter(SubTaskModel.id == sub_task_id)
                .first())

    def get_sub_tasks(self):
        return self.db.query(SubTaskModel).all()

    def get_sub_tasks(self, task_id: int):
        return (self.db.query(SubTaskModel)
                .filter(SubTaskModel.task_id == task_id)
                .all())

    def create_sub_task(self, sub_task: SubTaskModel):
        self.db.add(sub_task)

    def update_sub_task(self, sub_task: SubTaskModel):
        db_sub_task = self.get_sub_task(sub_task.id)
        for key, value in sub_task.__dict__.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                setattr(db_sub_task, key, value)

        # if it was the first time that the user hit progress button, then set start date of the subtask
        if sub_task.progress == 1:
            sub_task.start_date = datetime.now()

        # always keep completion of subtask synch with other timing parameters
        db_sub_task.is_completed = db_sub_task.progress == AppModel.default_pomodoro_time

        # check if the task was not set earlier, then synch it with completion of subtask
        if db_sub_task.end_date is None:
            db_sub_task.end_date = datetime.now() if db_sub_task.is_completed else None

    def update_sub_task_progression(self, sub_task_id: int, progress: int):
        sub_task = self.get_sub_task(sub_task_id)
        sub_task.progress = progress
        self.update_sub_task(sub_task)

    def delete_sub_task(self, sub_task: SubTaskModel):
        self.db.delete(sub_task)
