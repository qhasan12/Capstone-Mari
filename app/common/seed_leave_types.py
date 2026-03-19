from sqlalchemy.orm import Session
from app.leave.models import LeaveType, LeaveBalance
from app.employees.models import Employee


def seed_leave_types(db: Session):

    defaults = [
        {"name": "Sick", "default_allocation": 10},
        {"name": "Casual", "default_allocation": 10},
        {"name": "Bereavement", "default_allocation": 3},
    ]

    employees = db.query(Employee).filter(Employee.is_active == True).all()

    for item in defaults:

        leave_type = db.query(LeaveType).filter(
            LeaveType.name == item["name"]
        ).first()

        # Create LeaveType if not exists
        if not leave_type:
            leave_type = LeaveType(
                name=item["name"],
                default_allocation=item["default_allocation"],
                is_active=True
            )
            db.add(leave_type)
            db.flush()   # get leave_type.id

        # Create LeaveBalance for each employee
        for emp in employees:

            existing_balance = db.query(LeaveBalance).filter(
                LeaveBalance.employee_id == emp.id,
                LeaveBalance.leave_type_id == leave_type.id
            ).first()

            if not existing_balance:

                balance = LeaveBalance(
                    employee_id=emp.id,
                    leave_type_id=leave_type.id,
                    total_leaves=leave_type.default_allocation,
                    used_leaves=0,
                    remaining_leaves=leave_type.default_allocation,
                    is_active=True
                )

                db.add(balance)

    db.commit()