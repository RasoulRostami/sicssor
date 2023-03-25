from sqlalchemy.sql import exists
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
