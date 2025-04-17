"""
http error handler used via fastapi dependency injection
"""

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(
    _: Request,
    exc: HTTPException,
) -> JSONResponse:
    """this async function returns an http error"""
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)