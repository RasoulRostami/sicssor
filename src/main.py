import sys

from fastapi import FastAPI

from core import get_settings
from core.config import BASE_DIR

sys.path.append(BASE_DIR)

from src.app.v1.account.api import account_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Beauty salon booking web application",
)
app.include_router(account_router)
