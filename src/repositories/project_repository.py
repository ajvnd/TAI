from sqlalchemy.orm import Session
from src.models import ProjectModel


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_project(self, project_id: int):
        return self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()

    def get_projects(self):
        return self.db.query(ProjectModel).all()

    def create_project(self, project: ProjectModel):
        self.db.add(project)

    def update_project(self, project: ProjectModel):
        db_sub_task = self.get_project(project.id)
        for key, value in project.__dict__.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                setattr(db_sub_task, key, value)

    def delete_project(self, project: ProjectModel):
        self.db.delete(project)
