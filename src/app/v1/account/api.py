from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from src.core import get_settings
from src.core.authentication import get_current_user
from src.core.config import Settings
from src.db import User

from .schema import *
from .services import *

account_router = APIRouter(prefix="/v1/accounts", tags=["accounts"])


@account_router.post(
    "/register",
    status_code=201,
    response_model=RegisterSchema,
    response_model_exclude={"password", "confirm_password"},
)
def register(
    settings: Annotated[Settings, Depends(get_settings)],
    register: Annotated[RegisterSchema, Body()],
):
    user = User(email=register.email, password=register.password)
    service = UserServices(settings)
    valid, error = service.register_validation(user)
    if valid is True:
        service.register(user)
        return register
    raise HTTPException(status_code=422, detail=error)


@account_router.post("/login", response_model=TokenSchema, status_code=200)
async def login(
    settings: Annotated[Settings, Depends(get_settings)],
    login: Annotated[LoginSchema, Body()],
):
    service = UserServices(settings)
    token, error = await service.login(login.email, login.password)
    if error:
        raise HTTPException(status_code=422, detail=error)
    return TokenSchema(token=token)


@account_router.get("/profile", status_code=200, response_model=ProfileSchema)
async def profile_detail(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return ProfileSchema.factory(current_user)


@account_router.patch("/profile", status_code=200, response_model=ProfileSchema)
async def profile_detail(
    current_user: Annotated[User, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
    profile: Annotated[ProfileSchema, Body()],
):
    service = UserServices(settings)
    values = profile.dict(exclude_unset=True)
    user = await service.update(current_user, values)
    return ProfileSchema.factory(user)
