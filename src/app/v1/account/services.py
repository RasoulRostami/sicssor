from typing import Dict, Optional, Tuple

from passlib.hash import pbkdf2_sha256
from src.db import User
from src.db.repository import UserRepository


class UserServices:
    def __init__(self, settings) -> None:
        self._validated = False
        self._settings = settings
        self._repo = None

    def register_validation(self, user: User) -> Tuple[bool, Optional[Dict[str, str]]]:

        if self.repo.is_email_exists(user.email):
            return False, {"email": "email already exists."}
        self._validated = True
        return True, None

    def register(self, user: User) -> User:
        if self._validated:
            user.password = self.hash_password(user.password)
            return self.repo.create(user)
        raise ValueError("User hasn't been validated.")

    def hash_password(self, password):
        return pbkdf2_sha256.hash(password)

    @property
    def repo(self):
        if self._repo is None:
            self._repo = UserRepository(self._settings)
        return self._repo
