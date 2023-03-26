from datetime import date
from typing import Optional
from db import User
import validators
from pydantic import BaseModel, validator


class RegisterSchema(BaseModel):
    email: str
    password: str
    confirm_password: str

    @validator("email")
    def validate_email(cls, email):
        if validators.email(email) is True:
            return email
        raise ValueError("Email is invalid.")

    @validator("password")
    def validate_password(cls, password: str):
        lenght = 0
        has_digit = 0
        has_lower = 0
        has_capital = 0
        has_character = 0
        for p in password:
            lenght += 1
            if p.isdigit():
                has_digit = 1
            if p.islower():
                has_lower = 1
            if not p.islower() and p.isalpha():
                has_capital = 1
            if p.isascii() and not p.isalpha():
                has_character = 1
        lenght = 1 if lenght >= 8 else 0
        if all([has_capital, has_digit, has_lower, has_character, lenght]) is False:
            raise ValueError("Password is not strong.")
        return password

    @validator("confirm_password")
    def validate_confirm_password(cls, confirm_password, values, **kwargs):
        if values.get("password"):
            if confirm_password != values["password"]:
                raise ValueError("Confirm password is invalid.")
        return confirm_password


class LoginSchema(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, email):
        if validators.email(email) is True:
            return email
        raise ValueError("Email is invalid.")


class TokenSchema(BaseModel):
    token: str


class ProfileSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None

    @classmethod
    def factory(cls, user: User):
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            birthday=user.birthday,
            bio=user.bio,
            avatar=user.avatar,
        )


class UserSchema(ProfileSchema):
    email: str
    role: str
    is_superuser: bool
