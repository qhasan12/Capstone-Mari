from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_

from app.core.rbac import get_current_employee,has_permission,require_permission
from .models import Onboarding


# =====================================================
# CREATE
# =====================================================
# def create_onboarding(db: Session, data, current_user):

#     employee = get_current_employee(db, current_user)

#     require_permission(db, employee, "onboarding:create")

#     existing = db.query(Onboarding).filter(
#         Onboarding.employee_id == data.employee_id,
#         Onboarding.is_active == True
#     ).first()

#     if existing:
#         raise HTTPException(
#             400,
#             "Onboarding already exists for this employee"
#         )

#     onboarding = Onboarding(
#         employee_id=data.employee_id,
#         stage="Initiated"
#     )

#     db.add(onboarding)
#     db.commit()
#     db.refresh(onboarding)

#     return onboarding


# =====================================================
# GET ONE
# =====================================================
def get_onboarding_by_id(db: Session, onboarding_id: int, current_user):

    employee = get_current_employee(db, current_user)

    require_permission(db, employee, "onboarding:view")
    onboarding = db.query(Onboarding).filter(
        Onboarding.id == onboarding_id
    ).first()

    if not onboarding:
        raise HTTPException(404, "Onboarding not found")

    return onboarding


# =====================================================
# GET ALL (PAGINATION + SEARCH)
# =====================================================
def get_all_onboarding(
    db: Session,
    current_user,
    page: int = 1,
    per_page: int = 10,
    search: str | None = None,
    is_active: bool | None = True
):

    employee = get_current_employee(db, current_user)

    require_permission(db, employee, "onboarding:view")


    query = db.query(Onboarding)

    if is_active is not None:
        query = query.filter(Onboarding.is_active == is_active)

    if search:
        query = query.filter(
            Onboarding.stage.ilike(f"%{search}%")
        )

    total = query.count()

    records = (
        query
        .order_by(Onboarding.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return records, total


# =====================================================
# UPDATE
# =====================================================
def update_onboarding(db: Session, onboarding_id: int, data, current_user):

    employee = get_current_employee(db, current_user)
    require_permission(db, employee, "onboarding:update")

    onboarding = db.query(Onboarding).filter(
        Onboarding.id == onboarding_id
    ).first()

    if not onboarding:
        raise HTTPException(404, "Onboarding not found")

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(400, "No valid fields provided for update")

    for field, value in update_data.items():

        if value is None:
            raise HTTPException(400, f"{field} cannot be null")

        setattr(onboarding, field, value)

    # Smart stage logic
    if onboarding.orientation_sent:
        onboarding.stage = "Completed"
    elif onboarding.resources_allocated:
        onboarding.stage = "Resources Allocated"
    elif onboarding.email_created:
        onboarding.stage = "Email Created"
    elif onboarding.appointment_letter_generated:
        onboarding.stage = "Appointment Generated"

    db.commit()
    db.refresh(onboarding)

    return onboarding

# =====================================================
# DELETE
# =====================================================
def soft_delete_onboarding(db: Session, onboarding_id: int, current_user):

    employee = get_current_employee(db, current_user)

    require_permission(db, employee, "onboarding:delete")

    onboarding = db.query(Onboarding).filter(
        Onboarding.id == onboarding_id
    ).first()

    if not onboarding:
        raise HTTPException(404, "Onboarding not found")

    if not onboarding.is_active:
        raise HTTPException(400, "Onboarding already inactive")

    onboarding.is_active = False

    db.commit()

    return onboarding