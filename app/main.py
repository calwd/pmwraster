"""
Primary entry point to the application.
"""
from fastapi import FastAPI

from app.api_routes import router as router


def get_application() -> FastAPI:
    """this function returns the fastapi application"""
    application = FastAPI(
        title="Sample Code for Raster Queries",
    )

    application.include_router(router)
    return application


app = get_application()
