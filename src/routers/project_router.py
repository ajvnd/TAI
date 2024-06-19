from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import models
from src.repositories import ProjectRepository, TaskRepository
from src.schemas.project_schema import ProjectCreateSchema, ProjectUpdateSchema

router = APIRouter()


@router.get("/projects", status_code=status.HTTP_200_OK)
def get_projects(db: Session = Depends(models.get_db)):
    return ProjectRepository(db).get_projects()


@router.get("/projects/{project_id}", status_code=status.HTTP_200_OK)
def get_project(project_id: int, response: Response, db: Session = Depends(models.get_db)):
    project = ProjectRepository(db).get_project(project_id)
    if not project:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{project_id} not found"
    return project


@router.get("/projects/{project_id}/tasks", status_code=status.HTTP_200_OK)
def get_tasks(task_id: int, db: Session = Depends(models.get_db)):
    return TaskRepository(db).get_tasks(task_id)


@router.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project_create_schema: ProjectCreateSchema, db: Session = Depends(models.get_db)):
    project_create_schema = models.ProjectModel(**project_create_schema.dict())
    ProjectRepository(db).create_project(project_create_schema)
    db.commit()
    return project_create_schema.id


@router.put("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_project(project_id: int, project_update_schema: ProjectUpdateSchema, db: Session = Depends(models.get_db)):
    project_update_schema = models.ProjectModel(**project_update_schema.dict())
    project_update_schema.id = project_id
    ProjectRepository(db).update_project(project_update_schema)
    db.commit()


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, response: Response, db: Session = Depends(models.get_db)):
    project = ProjectRepository(db).get_project(project_id)
    if not project:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{project_id} not found"
    ProjectRepository(db).delete_project(project)
    db.commit()
