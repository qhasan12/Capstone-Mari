from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from app.employees.models import Employee
from app.permissions.models import RolePermission, Permission
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
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.employees.models import Employee
from app.permissions.models import RolePermission, Permission


# =========================
# GET CURRENT EMPLOYEE
# =========================
def get_current_employee(db: Session, current_user):

    # Ensure user has employee
    if not getattr(current_user, "employee_id", None):
        raise HTTPException(
            status_code=403,
            detail="User is not linked to an employee"
        )

    employee = db.query(Employee).filter(
        Employee.id == current_user.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee record not found"
        )

    if not employee.is_active:
        raise HTTPException(
            status_code=403,
            detail="Employee account is inactive"
        )


    return employee


# =========================
# PERMISSION CHECK
# =========================
#stops execution if permission is not found, otherwise returns None
def require_permission(db: Session, employee: Employee, permission_name: str):
    print("REQUIRE PERMISSION:", permission_name)
    print("EMPLOYEE ROLE ID:", employee.role_id)

    permission_exists = (
        db.query(Permission.id)
        .join(RolePermission, Permission.id == RolePermission.permission_id)
        .filter(
            RolePermission.role_id == employee.role_id,
            Permission.name == permission_name
        )
        .first()
        
    )
    if not permission_exists:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )
#conditional check that returns True/False instead of raising exception
def has_permission(db: Session, employee: Employee, permission_name: str) -> bool:
    permission_exists = (
        db.query(Permission.id)
        .join(RolePermission, Permission.id == RolePermission.permission_id)
        .filter(
            RolePermission.role_id == employee.role_id,
            Permission.name == permission_name
        )
        .first()
        
    )
    return permission_exists is not None