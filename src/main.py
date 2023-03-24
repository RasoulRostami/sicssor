import sys

from fastapi import FastAPI

from core.config import settings

sys.path.append(settings.BASE_DIR)
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Beauty salon booking web application",
)
