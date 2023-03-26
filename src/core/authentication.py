from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.app.v1.account.services import UserServices
from src.core import Settings
from src.db import User

from . import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/accounts/token")


async def decode_token(token, settings) -> User:
    service = UserServices(settings)
    user = await service.get_user({"token": token, "is_active": True})
    if user:
        return user
    raise HTTPException(status_code=403, detail="Token is invalid.")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    return await decode_token(token, settings)
