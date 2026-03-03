from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.hiring.schemas import (
    HiringRequestCreate,
    HiringRequestResponse,
    JobPostingCreate,
    JobPostingResponse
)
from app.hiring import service

router = APIRouter(tags=["Hiring"])

# -----------------------
# Job Posting Routes FIRST
# -----------------------

@router.post("/job-posting", response_model=JobPostingResponse)
def create_job_posting(
    job_data: JobPostingCreate,
    db: Session = Depends(get_db)
):
    return service.create_job_posting(db, job_data)


@router.get("/job-posting", response_model=List[JobPostingResponse])
def get_job_postings(db: Session = Depends(get_db)):
    return service.get_all_job_postings(db)


# -----------------------
# Hiring Request Routes
# -----------------------

@router.post("/", response_model=HiringRequestResponse)
def create_hiring_request(
    hiring_data: HiringRequestCreate,
    db: Session = Depends(get_db)
):
    return service.create_hiring_request(db, hiring_data)


@router.get("/", response_model=List[HiringRequestResponse])
def get_hiring_requests(db: Session = Depends(get_db)):
    return service.get_all_hiring_requests(db)


# ✅ Dynamic route ALWAYS LAST
@router.get("/{hiring_id}", response_model=HiringRequestResponse)
def get_hiring_request(hiring_id: int, db: Session = Depends(get_db)):
    hiring = service.get_hiring_request_by_id(db, hiring_id)
    if not hiring:
        raise HTTPException(status_code=404, detail="Hiring request not found")
    return hiring