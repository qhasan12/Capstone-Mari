from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Employee
from app.departments.models import Department
from app.roles.models import Role
from app.core.rbac import get_current_employee, require_permission,has_permission
from app.core.email import send_email
import uuid
from datetime import datetime, timedelta
# =========================
# READ ALL
# =========================
from sqlalchemy import or_

def get_employees(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = None
):

    employee = get_current_employee(db, current_user)

    query = db.query(Employee)

    if is_active is None:
        query = query.filter(Employee.is_active == True)
    else:
        query = query.filter(Employee.is_active == is_active)
    if search:
        query = query.filter(
            or_(
                Employee.full_name.ilike(f"%{search}%"),
                Employee.email.ilike(f"%{search}%")
            )
        )

    # print(require_permission(db, employee, "employee:view"))
    # Permission checks

    if has_permission(db, employee, "employee:view"):
        pass

    elif has_permission(db, employee, "employee:view_team"):
        query = query.filter(
            or_(
                Employee.id == employee.id,
                Employee.manager_id == employee.id
            )
        )
        #check later
        if has_permission(db, employee, "employee:view_self"):
            query = query.filter(
                or_(
                    Employee.id == employee.id,
                    Employee.manager_id == employee.id
                )
            )
    elif has_permission(db, employee, "employee:view_self"):
        query = query.filter(Employee.id == employee.id)

    else:
        raise HTTPException(403, "Not allowed to view employees")

    total = query.count()

    employees = (
        query
        .order_by(Employee.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return employees, total
# =========================
# READ ONE
# =========================
def get_employee_by_id(db: Session, employee_id: int, current_user):

    current_employee = get_current_employee(db, current_user)
    
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.is_active == True
    ).first()

    if not employee:
        raise HTTPException(404, "Employee not found")

    if has_permission(db, current_employee, "employee:view"):
        return employee

    if has_permission(db, current_employee, "employee:view_team"):

        if employee.manager_id == current_employee.id or employee.id == current_employee.id:
            return employee

    if has_permission(db, current_employee, "employee:view_self"):
        if employee.id == current_employee.id:
            return employee
    raise HTTPException(403, "Access denied")


# =========================
# CREATE
# =========================
def create_employee(db: Session, data, current_user):

    current_employee = get_current_employee(db, current_user)

    require_permission(db, current_employee, "employee:create")

    full_name = data.full_name.strip()

    # Email uniqueness
    if db.query(Employee).filter(Employee.email == data.email).first():
        raise HTTPException(400, "Email already exists")
    if db.query(Employee).filter(Employee.personal_email == data.personal_email).first():
        raise HTTPException(400, "Personal email already exists")

    # Department validation
    department = db.query(Department).filter(
        Department.id == data.department_id,
        Department.is_active == True
    ).first()

    if not department:
        raise HTTPException(400, "Invalid or inactive department")

    # Role validation
    role_obj = db.query(Role).filter(
        Role.id == data.role_id,
        Role.is_active == True
    ).first()

    if not role_obj:
        raise HTTPException(400, "Invalid or inactive role")

    # Manager validation
    if data.manager_id:

        if data.manager_id == current_employee.id:
            raise HTTPException(400, "Employee cannot be their own manager")

        manager = db.query(Employee).filter(
            Employee.id == data.manager_id,
            Employee.is_active == True
        ).first()

        if not manager:
            raise HTTPException(400, "Invalid manager")

    employee = Employee(**data.model_dump())
    employee.full_name = full_name

    db.add(employee)
    db.commit()
    db.refresh(employee)
    token=str(uuid.uuid4())
    employee.invite_token=token
    employee.invite_expiry=datetime.utcnow() + timedelta(days=7)
    db.commit()
    send_email(
    employee.personal_email,
    "HRMS Account Activation",
    f"Activate your account using this token:\n\n{token}"
    )
    #auto onboarding creation for new employee
    from app.onboarding.models import Onboarding
    onboarding = Onboarding(
        employee_id=employee.id,
        stage="Initiated"
    )
    db.add(onboarding)
    db.commit()
    return employee


# =========================
# UPDATE
# =========================
def update_employee(db: Session, employee_id: int, data, current_user):

    current_employee = get_current_employee(db, current_user)
    require_permission(db, current_employee, "employee:update")
    employee = get_employee_by_id(db, employee_id, current_user)

    # if has_permission(db, current_employee, "employee:update"):
    #     pass

    # elif has_permission(db, current_employee, "employee:update_self") and employee.id == current_employee.id:
    #     pass

    # else:
    #     raise HTTPException(403, "Not allowed to update this employee")

    update_data = data.model_dump(exclude_unset=True)

    if "full_name" in update_data:
        update_data["full_name"] = update_data["full_name"].strip()

    # Email uniqueness
    if "email" in update_data:

        exists = db.query(Employee).filter(
            Employee.email == update_data["email"],
            Employee.id != employee_id
        ).first()

        if exists:
            raise HTTPException(400, "Email already exists")

    # Department validation
    if "department_id" in update_data:

        department = db.query(Department).filter(
            Department.id == update_data["department_id"],
            Department.is_active == True
        ).first()

        if not department:
            raise HTTPException(400, "Invalid department")

    # Role validation
    if "role_id" in update_data:

        role_obj = db.query(Role).filter(
            Role.id == update_data["role_id"],
            Role.is_active == True
        ).first()

        if not role_obj:
            raise HTTPException(400, "Invalid role")

    # Manager validation
    if "manager_id" in update_data:

        manager_id = update_data["manager_id"]

        if manager_id == employee_id:
            raise HTTPException(400, "Employee cannot be their own manager")

        if manager_id:

            manager = db.query(Employee).filter(
                Employee.id == manager_id,
                Employee.is_active == True
            ).first()

            if not manager:
                raise HTTPException(400, "Invalid manager")

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


# =========================
# DELETE (SOFT DELETE)
# =========================
def delete_employee(db: Session, employee_id: int, current_user):

    current_employee = get_current_employee(db, current_user)
    require_permission(db, current_employee, "employee:delete")

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(404, "Employee not found")

    if not employee.is_active:
        raise HTTPException(400, "Employee already inactive")

    employee.is_active = False

    db.commit()
    db.refresh(employee)

    return employee