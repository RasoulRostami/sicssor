from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.sql import exists
from src.core.config import Settings
from src.db.session import get_async_session, get_session
from sqlalchemy.exc import NoResultFound
from ..models.user import User


class UserRepository:

    model = User

    def __init__(self, settings: Settings) -> None:
        self.session = get_session(settings)
        self.async_session = get_async_session(settings)

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return self.get_user_by_email(user.email)

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

    async def get(self, values: dict) -> Optional[User]:
        query = select(User).filter_by(**values).limit(1)
        result = await self._commit(query)
        try:
            return result.scalars().one()
        except NoResultFound:
            return None

    async def save(self, user: User, values: dict):
        query = update(User).where(User.id == user.id).values(values)
        await self._commit(query=query)

    async def _commit(self, query):
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(query)
                return result
