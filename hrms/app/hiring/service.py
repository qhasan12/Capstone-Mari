from sqlalchemy.orm import Session
from app.hiring.models import HiringRequest, JobPosting
from app.hiring.schemas import (
    HiringRequestCreate,
    HiringRequestResponse,
    JobPostingCreate,
    JobPostingResponse
)

# -----------------------
# Hiring Request Services
# -----------------------

def create_hiring_request(db: Session, hiring_data: HiringRequestCreate):
    hiring_request = HiringRequest(**hiring_data.dict())
    db.add(hiring_request)
    db.commit()
    db.refresh(hiring_request)
    return hiring_request


def get_all_hiring_requests(db: Session):
    return db.query(HiringRequest).all()


def get_hiring_request_by_id(db: Session, hiring_id: int):
    return db.query(HiringRequest).filter(HiringRequest.id == hiring_id).first()


# -----------------------
# Job Posting Services
# -----------------------

def create_job_posting(db: Session, job_data: JobPostingCreate):
    job_posting = JobPosting(**job_data.dict())
    db.add(job_posting)
    db.commit()
    db.refresh(job_posting)
    return job_posting


def get_all_job_postings(db: Session):
    return db.query(JobPosting).all()