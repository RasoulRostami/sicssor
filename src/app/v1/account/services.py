import uuid, hashlib
from typing import Dict, Optional, Tuple

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
            user.password = self._hash_password(user.password)
            return self.repo.create(user)
        raise ValueError("User hasn't been validated.")

    def login(self, email: str, password: str) -> Tuple[str, Optional[dict]]:
        hashed_password = self._hash_password(password)
        if self.repo.user_exists(email=email, password=hashed_password):
            user = self.repo.get_user_by_email(email)
            token = self._generate_token()
            self._set_token(user, token)
            return token, None
        return "", {"general": "email or password is invalid."}

    def _hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def _generate_token(self) -> str:
        return str(uuid.uuid4())

    def _set_token(self, user: User, token: str) -> None:
        self.repo.save(user, {"token": token})

    @property
    def repo(self) -> UserRepository:
        if self._repo is None:
            self._repo = UserRepository(self._settings)
        return self._repo
