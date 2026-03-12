from sqlalchemy.orm import Session

from app.departments.models import Department
from app.roles.models import Role
from app.employees.models import Employee
from app.auth.models import AuthUser
from app.auth.service import hash_password


def seed_initial_data(db: Session):

    # =========================
    # Department
    # =========================
    department = db.query(Department).filter(
        Department.name == "Administration"
    ).first()

    if not department:
        department = Department(name="Administration")
        db.add(department)
        db.commit()
        db.refresh(department)

    # =========================
    # Role (Super Admin)
    # =========================
    role = db.query(Role).filter(
        Role.title == "SA"
    ).first()

    if not role:
        role = Role(
            title="SA",
            name="SuperAdmin"
        )
        db.add(role)
        db.commit()
        db.refresh(role)

    # =========================
    # Employee
    # =========================
    employee = db.query(Employee).filter(
        Employee.email == "alishbahanif1@gmail.com"
    ).first()

    if not employee:
        employee = Employee(
            full_name="Alishba Hanif",
            personal_email="alishbave1@gmail.com",
            email="alishbahanif1@gmail.com",
            department_id=department.id,
            role_id=role.id,
            is_active=True
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)

    # =========================
    # Auth User
    # =========================
    user = db.query(AuthUser).filter(
        AuthUser.email == "alishbahanif1@gmail.com"
    ).first()

    if not user:
        user = AuthUser(
            email="alishbahanif1@gmail.com",
            password_hash=hash_password("Admin@123"),
            employee_id=employee.id,
            is_active=True
        )
        db.add(user)
        db.commit()