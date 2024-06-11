from sqlalchemy.orm import Session
from src import models


class Project:
    def __init__(self, db: Session):
        self.db = db

    def get_project(self, sub_task_id: int):
        return self.db.query(models.Project).filter(models.SubTask.id == sub_task_id).first()

    def get_projects(self):
        return self.db.query(models.Project).all()

    def create_project(self, project: models.Project):
        self.db.add(project)
        self.db.commit()

    def update_project(self, project: models.Project):
        db_sub_task = self.get_project(project.id)
        for key, value in project.__dict__.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                setattr(db_sub_task, key, value)
        self.db.commit()

    def delete_project(self, project: models.Project):
        self.db.delete(project)
        self.db.commit()
