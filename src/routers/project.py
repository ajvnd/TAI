from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import schemas, models
from src.repositories import ProjectRepository

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


@router.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(models.get_db)):
    project = models.ProjectModel(**project.dict())
    ProjectRepository(db).create_project(project)
    db.commit()
    return project.id


@router.put("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(models.get_db)):
    project = models.ProjectModel(**project.dict())
    project.id = project_id
    ProjectRepository(db).update_project(project)
    db.commit()


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, response: Response, db: Session = Depends(models.get_db)):
    project = ProjectRepository(db).get_project(project_id)
    if not project:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{project_id} not found"
    ProjectRepository(db).delete_project(project)
    db.commit()
