from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.employees.models import Employee
from app.permissions.models import RolePermission, Permission


# =========================
# SUPERADMIN CHECK
# =========================
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


# =========================
# GET CURRENT EMPLOYEE
# =========================
def get_current_employee(db: Session, current_user):

    if not current_user.employee_id:
        raise HTTPException(
            status_code=404,
            detail="Employee record not found"
        )

    employee = db.query(Employee).filter(
        Employee.id == current_user.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee record not found"
        )
    print("TOKEN USER:", current_user)
    return employee

# =========================
# REQUIRE PERMISSION
# =========================
def require_permission(db: Session, employee: Employee, permission_name: str):

    permission_exists = (
        db.query(RolePermission)
        .join(Permission)
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


# =========================
# HAS PERMISSION
# =========================
def has_permission(db: Session, employee: Employee, permission_name: str) -> bool:

    permission_exists = (
        db.query(RolePermission)
        .join(Permission)
        .filter(
            RolePermission.role_id == employee.role_id,
            Permission.name == permission_name
        )
        .first()
    )

    return permission_exists is not None
