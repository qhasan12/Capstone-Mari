from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.hiring.models import HiringRequest, JobPosting
from app.hiring.schemas import (
    HiringRequestCreate,
    HiringRequestUpdate,
    JobPostingCreate,
    JobPostingUpdate
)
# -----------------------
# Hiring Request Services
# -----------------------

# CREATE
def create_hiring_request(db: Session, hiring_data: HiringRequestCreate):
    hiring_request = HiringRequest(**hiring_data.model_dump())

    db.add(hiring_request)
    db.commit()
    db.refresh(hiring_request)

    return hiring_request


# READ ALL (only active)
def get_all_hiring_requests(db: Session):
    return (
        db.query(HiringRequest)
        .filter(HiringRequest.is_active == True)
        .order_by(HiringRequest.id)
        .all()
    )


# READ ONE
def get_hiring_request_by_id(db: Session, hiring_id: int):
    hiring = (
        db.query(HiringRequest)
        .filter(
            HiringRequest.id == hiring_id
        )
        .first()
    )

    if not hiring:
        raise HTTPException(status_code=404, detail="Hiring request not found")

    return hiring


# UPDATE (PATCH)
def update_hiring_request(db: Session, hiring_id: int, update_data: HiringRequestUpdate):

    hiring = get_hiring_request_by_id(db, hiring_id)

    if not hiring:
        raise HTTPException(status_code=404, detail="Hiring request not found")

    if hiring.status == "Closed":
        raise HTTPException(status_code=400, detail="Cannot modify a closed hiring request")

    update_fields = update_data.model_dump(exclude_unset=True)

    for field, value in update_fields.items():
        setattr(hiring, field, value)

    db.commit()
    db.refresh(hiring)

    return hiring


# SOFT DELETE
def delete_hiring_request(db: Session, hiring_id: int):

    hiring = (
        db.query(HiringRequest)
        .filter(
            HiringRequest.id == hiring_id,
            HiringRequest.is_active == True
        )
        .first()
    )

    if not hiring:
        raise HTTPException(status_code=404, detail="Hiring request not found")

    hiring.is_active = False
    db.commit()

    return {"message": "Hiring request deactivated successfully"}
# -----------------------
# Job Posting Services
# -----------------------
# CREATE
def create_job_posting(db: Session, job_data: JobPostingCreate):

    hiring = db.query(HiringRequest).filter(
        HiringRequest.id == job_data.hiring_request_id,
        HiringRequest.is_active == True
    ).first()

    if not hiring:
        raise HTTPException(status_code=404, detail="Hiring request not found")

    if job_data.closing_date < job_data.posted_date:
        raise HTTPException(
            status_code=400,
            detail="Closing date cannot be before posted date"
        )

    job_posting = JobPosting(**job_data.model_dump())

    db.add(job_posting)
    db.commit()
    db.refresh(job_posting)

    return job_posting


# READ ALL
def get_all_job_postings(db: Session):
    return (
        db.query(JobPosting)
        .filter(JobPosting.is_active == True)
        .order_by(JobPosting.id)
        .all()
    )


# READ ONE
def get_job_posting_by_id(db: Session, posting_id: int):

    posting = (
        db.query(JobPosting)
        .filter(
            JobPosting.id == posting_id
        )
        .first()
    )

    if not posting:
        raise HTTPException(status_code=404, detail="Job posting not found")

    return posting


# UPDATE
def update_job_posting(db: Session, posting_id: int, update_data: JobPostingUpdate):

    posting = get_job_posting_by_id(db, posting_id)

    if not posting:
        raise HTTPException(status_code=404, detail="Job posting not found")

    update_fields = update_data.model_dump(exclude_unset=True)

    if "closing_date" in update_fields:
        if posting.posted_date and update_fields["closing_date"] < posting.posted_date:
            raise HTTPException(
                status_code=400,
                detail="Closing date cannot be before posted date"
            )

    for field, value in update_fields.items():
        setattr(posting, field, value)

    db.commit()
    db.refresh(posting)

    return posting


# SOFT DELETE
def delete_job_posting(db: Session, posting_id: int):

    posting = (
        db.query(JobPosting)
        .filter(
            JobPosting.id == posting_id,
            JobPosting.is_active == True
        )
        .first()
    )

    if not posting:
        raise HTTPException(status_code=404, detail="Job posting not found")

    posting.is_active = False
    db.commit()

    return {"message": "Job posting deactivated successfully"}