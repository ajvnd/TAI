from sqlalchemy.orm import Session
from src.models import UserModel

user_model = UserModel


class User:
    def get_user(self, task_id: int, db: Session):
        return db.query(user_model).filter(user_model.id == task_id).first()

    def get_users(self, db: Session):
        return db.query(user_model).all()

    def create_user(self, db_user: user_model, db: Session):
        db.add(db_user)
        db.commit()

    def update_user(self, db_user: user_model, db: Session):
        task = db.query(user_model).filter(user_model.id == db_user.id).first()
        for key, value in db_user.__dict__.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                setattr(task, key, value)
        db.commit()

    def delete_user(self, db_user: user_model, db: Session):
        db.delete(db_user)
        db.commit()
