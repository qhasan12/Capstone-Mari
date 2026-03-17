from app.employees.service import (
    get_employees,
    get_employee_by_id,
    create_employee
)

def fetch_employees(db, current_user, page=1, per_page=10):
    employees, total = get_employees(db, current_user, page, per_page)
    return [
        {"id": e.id, "name": e.full_name, "email": e.email}
        for e in employees
    ]


def get_employee(db, current_user, employee_id: int):
    emp = get_employee_by_id(db, employee_id, current_user)
    return {"id": emp.id, "name": emp.full_name}


def create_employee_tool(db, current_user, data: dict):
    return create_employee(db, data, current_user)