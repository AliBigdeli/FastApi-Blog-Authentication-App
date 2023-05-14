from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

class DjangoException(Exception):
    def __init__(self, detail=None):
        self.detail = detail or "Server Error"
        super().__init__()

async def handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        detail = []
        for error in exc.errors():
            detail.append({"msg": error["msg"], "loc": error["loc"]})
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": detail},
        )
    elif isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": [{"msg": str(exc), "loc": []}]},
        )
    elif isinstance(exc, DjangoException):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc.detail)},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Server Error"},
        )