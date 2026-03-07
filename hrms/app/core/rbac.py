from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from app.employees.models import Employee
def ensure_superadmin(current_user):

    if (
        not current_user.employee
        or not current_user.employee.role
        or current_user.employee.role.title != "SA"
    ):
        raise HTTPException(
            status_code=403,
            detail="Only SuperAdmin is allowed to perform this action"
        )
        
        
def ensure_hr_or_sa(user):
    if user.role.name not in ["SuperAdmin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="HR or SuperAdmin access required"
        )


def ensure_manager(user):
    if user.role.name != "Manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required"
        )


# =========================
# HELPER: CURRENT EMPLOYEE
# =========================
def get_current_employee(db: Session, current_user):

    if not current_user.employee_id:
        raise HTTPException(403, "User is not linked to an employee")

    employee = db.query(Employee).filter(
        Employee.id == current_user.employee_id
    ).first()

    if not employee:
        raise HTTPException(404, "Employee record not found")

    if not employee.is_active:
        raise HTTPException(403, "Employee account is inactive")

    return employee