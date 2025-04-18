"""
Primary entry point to the application.
"""
from fastapi import FastAPI

from app.api_routes import router as router
from app.config import app_config


def get_application() -> FastAPI:
    """this function returns the fastapi application"""
    application = FastAPI(
        title=app_config.application_name,
    )

    application.include_router(router)
    return application


app = get_application()
