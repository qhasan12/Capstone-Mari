from fastapi import FastAPI
from app.core.database import engine, Base
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


# (add other routers as needed)

app = FastAPI(title="HRMS API")

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
# Auto create tables (Django-like behavior)
# Base.metadata.create_all(bind=engine)

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