from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.database import engine, Base
<<<<<<< HEAD
from app.common.schemas import APIResponse


# IMPORTANT: import all models so SQLAlchemy registers them
from app.leave import models as leave_models
from app.onboarding import models as onboarding_models
from app.resignation import models as resignation_models
=======
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

# IMPORTANT: import all models so SQLAlchemy registers them
from app.departments import models as department_models
from app.employees import models as employee_models
from app.hiring import models as hiring_models
from app.roles import models as role_models
from app.common.schemas import APIResponse  
from app.employees.routes import router as employee_router
from app.departments.routes import router as department_router
from app.hiring.routes import router as hiring_router
from app.roles.routes import router as role_router
from app.training.routes import router as training_router

from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler
)
>>>>>>> dev-branch


# Routers
from app.leave.routes import router as leave_router
from app.onboarding.routes import router as onboarding_router
from app.resignation.routes import router as resignation_router


app = FastAPI(title="HRMS API")

<<<<<<< HEAD

# ==========================================================
# GLOBAL EXCEPTION HANDLERS
# ==========================================================

=======
>>>>>>> dev-branch
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
<<<<<<< HEAD


=======
>>>>>>> dev-branch
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
<<<<<<< HEAD


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


=======
# Auto create tables (Django-like behavior)
# Base.metadata.create_all(bind=engine)
>>>>>>> dev-branch

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
<<<<<<< HEAD
    resignation_router,
    prefix="/api/v1/resignations",
    tags=["Resignation"]
)
=======
    hiring_router,
    prefix="/api/v1/hiring",
    tags=["Hiring"]
)
app.include_router(
    role_router,
    prefix="/api/v1/roles",
    tags=["Roles"]
)
# Auto create tables (Django-like behavior)
Base.metadata.create_all(bind=engine)
print("CONNECTED TO:", engine.url)

app.include_router(
    employee_router,
    prefix="/api/v1/employees",
    tags=["Employees"]
)
app.include_router(
    department_router,
    prefix="/api/v1/departments",
    tags=["Departments"]
)
app.include_router(
    hiring_router,
    prefix="/api/v1/hiring",
    tags=["Hiring"]
)
app.include_router(
    role_router,
    prefix="/api/v1/roles",
    tags=["Roles"]
)
app.include_router(
    training_router,
    prefix="/api/v1/trainings",
    tags=["Trainings"]
)


app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
>>>>>>> dev-branch
