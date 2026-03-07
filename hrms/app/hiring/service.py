from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.hiring.models import HiringRequest, JobPosting
from app.hiring.schemas import (
    HiringRequestCreate,
    HiringRequestUpdate,
    JobPostingCreate,
    JobPostingUpdate
)

from app.core.rbac import get_current_employee


# -----------------------
# Hiring Request Services
# -----------------------

# CREATE
def create_hiring_request(db: Session, hiring_data: HiringRequestCreate, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to create hiring requests")

    hiring_request = HiringRequest(**hiring_data.model_dump())

    db.add(hiring_request)
    db.commit()
    db.refresh(hiring_request)

    return hiring_request


# READ ALL
def get_all_hiring_requests(db: Session, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to view hiring requests")

    return (
        db.query(HiringRequest)
        .filter(HiringRequest.is_active == True)
        .order_by(HiringRequest.id)
        .all()
    )


# READ ONE
def get_hiring_request_by_id(db: Session, hiring_id: int, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to view hiring requests")

    hiring = (
        db.query(HiringRequest)
        .filter(HiringRequest.id == hiring_id)
        .first()
    )

    if not hiring:
        raise HTTPException(404, "Hiring request not found")

    return hiring


# UPDATE
def update_hiring_request(
    db: Session,
    hiring_id: int,
    update_data: HiringRequestUpdate,
    current_user
):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to update hiring requests")

    hiring = (
        db.query(HiringRequest)
        .filter(HiringRequest.id == hiring_id)
        .first()
    )

    if not hiring:
        raise HTTPException(404, "Hiring request not found")

    if hiring.status == "Closed":
        raise HTTPException(400, "Cannot modify a closed hiring request")

    update_fields = update_data.model_dump(exclude_unset=True)

    for field, value in update_fields.items():
        setattr(hiring, field, value)

    db.commit()
    db.refresh(hiring)

    return hiring


# DELETE (SOFT DELETE)
def delete_hiring_request(db: Session, hiring_id: int, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to delete hiring requests")

    hiring = (
        db.query(HiringRequest)
        .filter(
            HiringRequest.id == hiring_id,
            HiringRequest.is_active == True
        )
        .first()
    )

    if not hiring:
        raise HTTPException(404, "Hiring request not found")

    hiring.is_active = False

    db.commit()

    return {"message": "Hiring request deactivated successfully"}


# -----------------------
# Job Posting Services
# -----------------------

# CREATE
def create_job_posting(db: Session, job_data: JobPostingCreate, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to create job postings")

    hiring = db.query(HiringRequest).filter(
        HiringRequest.id == job_data.hiring_request_id,
        HiringRequest.is_active == True
    ).first()

    if not hiring:
        raise HTTPException(404, "Hiring request not found")

    if job_data.closing_date < job_data.posted_date:
        raise HTTPException(
            400,
            "Closing date cannot be before posted date"
        )

    job_posting = JobPosting(**job_data.model_dump())

    db.add(job_posting)
    db.commit()
    db.refresh(job_posting)

    return job_posting


# READ ALL
def get_all_job_postings(db: Session, current_user):

    # Everyone logged in can view
    get_current_employee(db, current_user)

    return (
        db.query(JobPosting)
        .filter(JobPosting.is_active == True)
        .order_by(JobPosting.id)
        .all()
    )


# READ ONE
def get_job_posting_by_id(db: Session, posting_id: int, current_user):

    get_current_employee(db, current_user)

    posting = (
        db.query(JobPosting)
        .filter(JobPosting.id == posting_id)
        .first()
    )

    if not posting:
        raise HTTPException(404, "Job posting not found")

    return posting


# UPDATE
def update_job_posting(
    db: Session,
    posting_id: int,
    update_data: JobPostingUpdate,
    current_user
):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to update job postings")

    posting = (
        db.query(JobPosting)
        .filter(JobPosting.id == posting_id)
        .first()
    )

    if not posting:
        raise HTTPException(404, "Job posting not found")

    update_fields = update_data.model_dump(exclude_unset=True)

    if "closing_date" in update_fields:
        if posting.posted_date and update_fields["closing_date"] < posting.posted_date:
            raise HTTPException(
                400,
                "Closing date cannot be before posted date"
            )

    for field, value in update_fields.items():
        setattr(posting, field, value)

    db.commit()
    db.refresh(posting)

    return posting


# DELETE (SOFT DELETE)
def delete_job_posting(db: Session, posting_id: int, current_user):

    employee = get_current_employee(db, current_user)
    role = employee.role.title

    if role not in ["SA", "HR"]:
        raise HTTPException(403, "Not allowed to delete job postings")

    posting = (
        db.query(JobPosting)
        .filter(
            JobPosting.id == posting_id,
            JobPosting.is_active == True
        )
        .first()
    )

    if not posting:
        raise HTTPException(404, "Job posting not found")

    posting.is_active = False

    db.commit()

    return {"message": "Job posting deactivated successfully"}