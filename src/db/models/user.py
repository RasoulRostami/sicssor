import enum

from sqlalchemy import Boolean, Column, Date, Enum, String, Text

from ..base_class import Base


class User(Base):
    class RoleChoices(enum.Enum):
        CUSTOMER = 1
        EMPLOYEE = 2
        MANAGER = 3
        SUPERUSER = 4

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(150), nullable=True)
    birthday = Column(Date(), nullable=True)
    bio = Column(Text(), nullable=True)
    role = Column(Enum(RoleChoices), default=RoleChoices.CUSTOMER)
    token = Column(String(150), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    avatar = Column(String(200), nullable=True)
