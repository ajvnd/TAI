from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from src import schemas
from src.models import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users", status_code=status.HTTP_200_OK, tags=["users"])
def get_users(db: Session = Depends(get_db)):
    pass


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
def get_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    pass


@router.post("/users", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(task: schemas.UserCreate, db: Session = Depends(get_db)):
    pass


@router.put("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def update_user(user_id: int, task: schemas.UserUpdate, db: Session = Depends(get_db)):
    pass


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    pass
