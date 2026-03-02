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

from app.employees.routes import router as employee_router
from app.leave.routes import router as leave_router
from app.employees.routes import router as employee_router
from app.departments.routes import router as department_router
from app.hiring.routes import router as hiring_router
# (add other routers as needed)

app = FastAPI(title="HRMS API")

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
    leave_router,
    prefix="/api/v1/leaves",
    tags= ["Leave"]
)

