from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.database import engine, Base
from app.common.schemas import APIResponse


# IMPORTANT: import all models so SQLAlchemy registers them
from app.leave import models as leave_models
from app.onboarding import models as onboarding_models
from app.resignation import models as resignation_models


# Routers
from app.leave.routes import router as leave_router
from app.onboarding.routes import router as onboarding_router
from app.resignation.routes import router as resignation_router


app = FastAPI(title="HRMS API")


# ==========================================================
# GLOBAL EXCEPTION HANDLERS
# ==========================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            code=exc.status_code,
            message=exc.detail,
            data=None,
            errors=None
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=APIResponse(
            code=422,
            message="Validation error",
            data=None,
            errors=exc.errors()
        ).model_dump()
    )


# Optional: Catch All Unhandled Errors (Recommended)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            code=500,
            message="Internal server error",
            data=None,
            errors=str(exc)  # You can remove this in production
        ).model_dump()
    )


# ==========================================================
# INCLUDE ROUTERS
# ==========================================================



app.include_router(
    leave_router,
    prefix="/api/v1/leaves",
    tags=["Leave"]
)

app.include_router(
    onboarding_router,
    prefix="/api/v1/onboarding",
    tags=["Onboarding"]
)

app.include_router(
    resignation_router,
    prefix="/api/v1/resignations",
    tags=["Resignation"]
)