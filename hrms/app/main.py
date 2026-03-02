from fastapi import FastAPI
from app.core.database import engine, Base

# IMPORTANT: import all models so SQLAlchemy registers them
from app.departments import models as department_models
from app.employees import models as employee_models
from app.hiring import models as hiring_models
from app.leave import models as leave_models
from app.onboarding import models as onboarding_models
from app.resignation import models as resignation_models
from app.roles import models as role_models
from app.training import models as training_models
from app.common.schemas import APIResponse  
from app.employees.routes import router as employee_router
from app.departments.routes import router as department_router
from app.hiring.routes import router as hiring_router
from app.roles.routes import router as role_router
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import validation_exception_handler
from fastapi import HTTPException
from starlette.requests import Request
from starlette import status
from fastapi.responses import JSONResponse
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