from sqlalchemy.sql import exists
from typing import Optional
from src.core.config import Settings
from src.db.session import get_session

from ..models.user import User


class UserRepository:

    model = User

    def __init__(self, settings: Settings) -> None:
        self.session = get_session(settings)

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

    def is_email_exists(self, email: str) -> bool:
        if self.session.query(exists().where(User.email == email)).scalar():
            return True
        return False

    def user_exists(self, email: str, password: str) -> bool:
        if self.session.query(
            exists().where(User.email == email, User.password == password)
        ).scalar():
            return True
        return False

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter_by(email=email).first()

    def get_user_by_id(self, pk: str) -> User:
        user = self.session.get(User, pk)
        self.session.commit()
        return user

    def refresh_db(self, user: User) -> User:
        self.session.refresh(user)
        return user

    def save(self, user: User, values: dict):
        self.session.query(self.model).filter(User.id == user.id).update(values)
        self.session.commit()
