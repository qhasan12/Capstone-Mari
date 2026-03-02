from fastapi import FastAPI
from app.employees.routes import router as employee_router

app = FastAPI(title="HRMS API")

app.include_router(employee_router, prefix="/api/v1/employees", tags=["Employees"])