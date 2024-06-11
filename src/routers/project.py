from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import schemas, models, repositories

router = APIRouter()


@router.get("/projects", status_code=status.HTTP_200_OK)
def get_projects(db: Session = Depends(models.get_db)):
    return repositories.SubTask(db).get_sub_tasks()


@router.get("/project/{project_id}", status_code=status.HTTP_200_OK)
def get_project(project_id: int, response: Response, db: Session = Depends(models.get_db)):
    project = repositories.Project(db).get_project(project_id)
    if not project:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{project_id} not found"
    return project


@router.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(models.get_db)):
    project = models.Project(**project.dict())
    repositories.Project(db).create_project(project)


@router.put("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(models.get_db)):
    project = models.Project(**project.dict())
    project.id = project_id
    repositories.Project(db).update_project(project)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, response: Response, db: Session = Depends(models.get_db)):
    project = repositories.Project(db).get_project(project_id)
    if not project:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"{project_id} not found"
    repositories.Project(db).delete_project(project)
