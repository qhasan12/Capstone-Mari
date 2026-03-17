from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.common.seed_roles import seed_roles
from app.core.database import SessionLocal
from app.core.database import engine, Base
from app.common.schemas import APIResponse

# IMPORTANT: import all models so SQLAlchemy registers them
from app.leave import models as leave_models
from app.onboarding import models as onboarding_models
from app.resignation import models as resignation_models
from app.departments import models as department_models
from app.employees import models as employee_models
from app.hiring import models as hiring_models
from app.roles import models as role_models
from app.auth.models import AuthUser
from app.permissions import models as permission_models
from app.training import models as training_models

# Routers
from app.leave.routes import router as leave_router
from app.onboarding.routes import router as onboarding_router
from app.resignation.routes import router as resignation_router
from app.departments.routes import router as department_router
from app.employees.routes import router as employee_router
from app.hiring.routes import router as hiring_router
from app.roles.routes import router as role_router
from app.training.routes import router as training_router
from app.auth.routes import router as auth_router
from app.common.seed_permissions import seed_permissions
from app.common.seed_role_permissions import seed_role_permissions
from app.common.seed_leave_types import seed_leave_types
from app.common.seed import seed_initial_data
# ✅ CREATE APP HERE
app = FastAPI(title="HRMS API", version="1.0")
#adding seed data for roles

@app.on_event("startup")
def startup_event():

    # ✅ CREATE TABLES FIRST
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # ✅ THEN RUN SEEDS
    seed_roles(db)
    seed_permissions(db)
    seed_role_permissions(db)
    seed_leave_types(db)
    seed_initial_data(db)


    db.close()
# ==============================
# Global Exception Handlers
# ==============================

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


from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    errors = []

    for err in exc.errors():
        errors.append({
            "field": ".".join(map(str, err["loc"])),
            "message": str(err["msg"])
        })

    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "Validation error",
            "data": None,
            "errors": errors
        }
    )

# ==============================
# DB Connection Check
# ==============================

print("CONNECTED TO:", engine.url)


# ==============================
# Register Routers
# ==============================

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])

app.include_router(leave_router, prefix="/api/v1/leaves", tags=["Leave"])

app.include_router(onboarding_router, prefix="/api/v1/onboarding", tags=["Onboarding"])

app.include_router(resignation_router, prefix="/api/v1/resignations", tags=["Resignation"])

app.include_router(hiring_router, prefix="/api/v1/hiring", tags=["Hiring"])

app.include_router(role_router, prefix="/api/v1/roles", tags=["Roles"])

app.include_router(employee_router, prefix="/api/v1/employees", tags=["Employees"])

app.include_router(department_router, prefix="/api/v1/departments", tags=["Departments"])

app.include_router(training_router, prefix="/api/v1/trainings", tags=["Trainings"])

app.include_router(employee_router, prefix="/employees")