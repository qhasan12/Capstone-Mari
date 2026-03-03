from fastapi.responses import JSONResponse
<<<<<<< HEAD
from fastapi import Request
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
=======
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException


# Handle HTTPException (404, 400 etc.)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None,
            "errors": None
        },
    )


# Handle Validation Errors (422)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "message": "Validation error",
            "data": None,
>>>>>>> dev-branch
            "errors": exc.errors()
        },
    )