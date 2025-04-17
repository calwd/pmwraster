"""
Primary entry point to the flight log service
"""
from fastapi import FastAPI

from app.api.routes.api import router as api_router


def get_application() -> FastAPI:
    """this function returns the fastapi application"""
    application = FastAPI(
        title="Sample Code for Raster Queries",
    )

    application.include_router(api_router)
    return application


app = get_application()
