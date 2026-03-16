from sqlalchemy.orm import Session

from app.departments.models import Department
from app.roles.models import Role
from app.employees.models import Employee
from app.auth.models import AuthUser
from app.auth.service import hash_password
from app.leave.models import LeaveType, LeaveBalance
from app.onboarding.models import Onboarding


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
    # Roles
    # =========================
    roles_data = [
        {"title": "SA", "name": "SuperAdmin"},
        {"title": "HR", "name": "Human Resource"},
        {"title": "MGR", "name": "Manager"},
        {"title": "EMP", "name": "Employee"},
    ]

    roles = {}

    for r in roles_data:

        role = db.query(Role).filter(
            Role.title == r["title"]
        ).first()

        if not role:
            role = Role(
                title=r["title"],
                name=r["name"]
            )
            db.add(role)
            db.commit()
            db.refresh(role)

        roles[r["title"]] = role

    # =========================
    # Employees
    # =========================
    employees_data = [
        {
            "full_name": "Admin User",
            "email": "admin@company.com",
            "personal_email": "admin@gmail.com",
            "role": "SA",
            "password": "123"
        },
        {
            "full_name": "HR User",
            "email": "hr@company.com",
            "personal_email": "hr@gmail.com",
            "role": "HR",
            "password": "123"
        },
        {
            "full_name": "Manager User",
            "email": "manager@company.com",
            "personal_email": "manager@gmail.com",
            "role": "MGR",
            "password": "123"
        },
        {
            "full_name": "Employee User",
            "email": "employee@company.com",
            "personal_email": "employee@gmail.com",
            "role": "EMP",
            "password": "123"
        },
    ]

    for emp in employees_data:

        # =========================
        # Employee
        # =========================
        employee = db.query(Employee).filter(
            Employee.email == emp["email"]
        ).first()

        if not employee:

            employee = Employee(
                full_name=emp["full_name"],
                email=emp["email"],
                personal_email=emp["personal_email"],
                department_id=department.id,
                role_id=roles[emp["role"]].id,
                is_active=True
            )

            db.add(employee)
            db.commit()
            db.refresh(employee)

            # =========================
            # Create Leave Balances
            # =========================
            leave_types = db.query(LeaveType).filter(
                LeaveType.is_active == True
            ).all()

            for lt in leave_types:

                existing_balance = db.query(LeaveBalance).filter(
                    LeaveBalance.employee_id == employee.id,
                    LeaveBalance.leave_type_id == lt.id
                ).first()

                if not existing_balance:

                    balance = LeaveBalance(
                        employee_id=employee.id,
                        leave_type_id=lt.id,
                        total_leaves=lt.default_allocation,
                        used_leaves=0,
                        remaining_leaves=lt.default_allocation,
                        is_active=True
                    )

                    db.add(balance)

            db.commit()
            

        # =========================
        # Auth User
        # =========================
        user = db.query(AuthUser).filter(
            AuthUser.email == emp["email"]
        ).first()

        if not user:

            user = AuthUser(
                email=emp["email"],
                password_hash=hash_password(emp["password"]),
                employee_id=employee.id,
                is_active=True
            )

            db.add(user)
            db.commit()
            
                # ========================
        # onboarding of employee
        # ========================
        onboarding = db.query(Onboarding).filter(
            Onboarding.employee_id == employee.id
        ).first()
    

        if not onboarding:
            onboarding = Onboarding(
                employee_id=employee.id,
                status="Initiated",
                is_active=True
            )
            db.add(onboarding)
            db.commit()
            db.refresh(onboarding)
