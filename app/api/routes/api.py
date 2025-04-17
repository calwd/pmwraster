
"""
This module contains the API routes for the application.
"""

from fastapi import APIRouter
from app.api.routes.imagery import router as imagery_router


router = APIRouter()
router.include_router(imagery_router, tags=["imagery"], prefix="/imagery")
