from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from .models import Training, TrainingAssignment
from app.employees.models import Employee
from app.core.rbac import get_current_employee, has_permission,require_permission


# =====================================================
# CREATE
# =====================================================

def create_training(db: Session, data, current_user):

    creator = get_current_employee(db, current_user)

    require_permission(db, creator,"training:create")
    # =========================
    # Prevent duplicate training
    # =========================
    existing = db.query(Training).filter(
        Training.title == data.title,
        Training.training_date == data.training_date,
        Training.is_active == True
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Training with same title and date already exists"
        )

    training = Training(
        title=data.title,
        description=data.description,
        training_date=data.training_date,
        created_by=creator.id,
        is_active=True
    )

    db.add(training)
    db.flush()

    employee_ids = set()

    targets = data.assign_to

    # direct employees
    if targets.employees:
        employee_ids.update(targets.employees)

    # departments
    if targets.departments:
        dept_emps = db.query(Employee.id).filter(
            Employee.department_id.in_(targets.departments)
        ).all()

        employee_ids.update([e[0] for e in dept_emps])

    # roles
    if targets.roles:
        role_emps = db.query(Employee.id).filter(
            Employee.role_id.in_(targets.roles)
        ).all()

        employee_ids.update([e[0] for e in role_emps])

    # managers teams
    if targets.managers:
        team_emps = db.query(Employee.id).filter(
            Employee.manager_id.in_(targets.managers)
        ).all()

        employee_ids.update([e[0] for e in team_emps])

    # entire company
    if targets.all_employees:
        all_emps = db.query(Employee.id).all()
        employee_ids.update([e[0] for e in all_emps])

    if not employee_ids:
        raise HTTPException(400, "No employees resolved")

    assignments = [
        TrainingAssignment(
            training_id=training.id,
            employee_id=eid
        )
        for eid in employee_ids
    ]

    db.add_all(assignments)

    db.commit()
    db.refresh(training)

    return training


# =====================================================
# LIST
# =====================================================

def get_trainings(
    db: Session,
    current_user,
    page: int,
    per_page: int,
    search: str | None,
    is_active: bool | None=True
):

    employee = get_current_employee(db, current_user)
    if not (
        has_permission(db,employee, "training:view") or
        has_permission(db, employee, "training:view_team") or
        has_permission(db, employee, "training:view_self")
    ):

        raise HTTPException(401,"Permission denied")

    query = db.query(Training)

    if is_active is not None:
        query = query.filter(Training.is_active == is_active)

    if search:
        query = query.filter(Training.title.ilike(f"%{search}%"))


    # SA / HR → all trainings
    if has_permission(db, employee, "training:view"):
        pass

    # Manager → team + self
    elif has_permission(db, employee, "training:view_team"):

        team_ids = db.query(Employee.id).filter(
            Employee.manager_id == employee.id
        )

        query = query.join(TrainingAssignment).filter(
            or_(
                TrainingAssignment.employee_id == employee.id,
                TrainingAssignment.employee_id.in_(team_ids)
            )
        )

    # Employee → self only
    elif has_permission(db, employee, "training:view_self"):

        query = query.join(TrainingAssignment).filter(
            TrainingAssignment.employee_id == employee.id
        )
    total = query.count()

    trainings = (
        query
        .order_by(Training.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return trainings, total


# =====================================================
# GET ONE
# =====================================================

def get_training_by_id(db: Session, training_id: int, current_user):

    employee =get_current_employee(db, current_user)
    if not (
        has_permission(db, employee, "training:view") or
        has_permission(db, employee, "training:view_team") or
        has_permission(db, employee, "training:view_self")
    ):
        raise HTTPException(403, "Permission denied")

    training = db.query(Training).filter(
        Training.id == training_id
    ).first()
    if not training:
        raise HTTPException(
            status_code=404,
            detail="Training not found"
        )

    # SA / HR
    if has_permission(db, employee, "training:view"):
        return training

    # Manager → team + self
    if has_permission(db, employee, "training:view_team"):

        team_ids = db.query(Employee.id).filter(
            Employee.manager_id == employee.id
        )

        assignment = db.query(TrainingAssignment).filter(
            TrainingAssignment.training_id == training_id,
            or_(
                TrainingAssignment.employee_id == employee.id,
                TrainingAssignment.employee_id.in_(team_ids)
            )
        ).first()

        if not assignment:
            raise HTTPException(403, "Not allowed")

        return training

    # Employee → self only
    if has_permission(db, employee, "training:view_self"):

        assignment = db.query(TrainingAssignment).filter(
            TrainingAssignment.training_id == training_id,
            TrainingAssignment.employee_id == employee.id
        ).first()

        if not assignment:
            raise HTTPException(403, "Not allowed")

    return training


# =====================================================
# UPDATE
# =====================================================


def update_training(db: Session, training_id: int, data, current_user):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee,"training:update")

    training = db.query(Training).filter(
        Training.id == training_id
    ).first()
    
    if training.title==data.title:
        raise HTTPException(
            status_code=400,
            detail="Training with same title or date already exists"
        )

    if not training:
        raise HTTPException(404, "Training not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(training, key, value)

    db.commit()
    db.refresh(training)

    return training


# =====================================================
# DELETE (SOFT DELETE)
# =====================================================

def delete_training(db: Session, training_id: int, current_user):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "training:delete")

    if employee.role.title not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed")

    training = db.query(Training).filter(
        Training.id == training_id
    ).first()

    if not training:
        raise HTTPException(404, "Training not found")

    if not training.is_active:
        raise HTTPException(400, "Training already inactive")

    training.is_active = False

    db.commit()
    db.refresh(training)

    return training