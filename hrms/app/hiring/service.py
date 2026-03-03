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

def create_hiring_request(db: Session, hiring_data: HiringRequestCreate):
    hiring_request = HiringRequest(**hiring_data.model_dump())
    db.add(hiring_request)
    db.commit()
    db.refresh(hiring_request)
    return hiring_request


def get_all_hiring_requests(db: Session):
    return db.query(HiringRequest).all()


def get_hiring_request_by_id(db: Session, hiring_id: int):
    hiring = db.query(HiringRequest).filter(
        HiringRequest.id == hiring_id
    ).first()
    if not hiring:
        raise HTTPException(404, "Hiring request not found")
    return hiring


def update_hiring_request(
    db: Session,
    hiring_id: int,
    update_data: HiringRequestUpdate
):
    hiring = db.query(HiringRequest).filter(
        HiringRequest.id == hiring_id
    ).first()

    if not hiring:
        raise HTTPException(404, "Hiring request not found")

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(hiring, field, value)

    db.commit()
    db.refresh(hiring)
    return hiring


def delete_hiring_request(db: Session, hiring_id: int):
    hiring = db.query(HiringRequest).filter(
        HiringRequest.id == hiring_id
    ).first()

    if not hiring:
        raise HTTPException(404, "Hiring request not found")

    db.delete(hiring)
    db.commit()
    return {"message": "Hiring request deleted"}


# -----------------------
# Job Posting Services
# -----------------------

def create_job_posting(db: Session, job_data: JobPostingCreate):
    job_posting = JobPosting(**job_data.model_dump())
    db.add(job_posting)
    db.commit()
    db.refresh(job_posting)
    return job_posting


def get_all_job_postings(db: Session):
    return db.query(JobPosting).all()


def get_job_posting_by_id(db: Session, posting_id: int):
    posting = db.query(JobPosting).filter(
        JobPosting.id == posting_id
    ).first()
    if not posting:
        raise HTTPException(404, "Job posting not found")
    return posting


def update_job_posting(
    db: Session,
    posting_id: int,
    update_data: JobPostingUpdate
):
    posting = db.query(JobPosting).filter(
        JobPosting.id == posting_id
    ).first()

    if not posting:
        raise HTTPException(404, "Job posting not found")

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(posting, field, value)

    db.commit()
    db.refresh(posting)
    return posting


def delete_job_posting(db: Session, posting_id: int):
    posting = db.query(JobPosting).filter(
        JobPosting.id == posting_id
    ).first()

    if not posting:
        raise HTTPException(404, "Job posting not found")

    db.delete(posting)
    db.commit()
    return {"message": "Job posting deleted"}