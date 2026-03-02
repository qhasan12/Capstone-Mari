from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.hiring.schemas import (
    HiringRequestCreate,
    HiringRequestResponse,
    HiringRequestUpdate,
    JobPostingCreate,
    JobPostingResponse,
    JobPostingUpdate
)
from app.hiring import service

router = APIRouter(tags=["Hiring"])

# =====================================================
# Job Posting Routes (STATIC FIRST)
# =====================================================

@router.post("/job-posting", response_model=JobPostingResponse)
def create_job_posting(
    job_data: JobPostingCreate,
    db: Session = Depends(get_db)
):
    return service.create_job_posting(db, job_data)


@router.get("/job-posting", response_model=List[JobPostingResponse])
def get_job_postings(db: Session = Depends(get_db)):
    return service.get_all_job_postings(db)


@router.get("/job-posting/{posting_id}", response_model=JobPostingResponse)
def get_job_posting(posting_id: int, db: Session = Depends(get_db)):
    return service.get_job_posting_by_id(db, posting_id)


@router.put("/job-posting/{posting_id}", response_model=JobPostingResponse)
def update_job_posting(
    posting_id: int,
    update_data: JobPostingUpdate,
    db: Session = Depends(get_db)
):
    return service.update_job_posting(db, posting_id, update_data)


@router.delete("/job-posting/{posting_id}")
def delete_job_posting(posting_id: int, db: Session = Depends(get_db)):
    return service.delete_job_posting(db, posting_id)


# =====================================================
# Hiring Request Routes
# =====================================================

@router.post("/", response_model=HiringRequestResponse)
def create_hiring_request(
    hiring_data: HiringRequestCreate,
    db: Session = Depends(get_db)
):
    return service.create_hiring_request(db, hiring_data)


@router.get("/", response_model=List[HiringRequestResponse])
def get_hiring_requests(db: Session = Depends(get_db)):
    return service.get_all_hiring_requests(db)


@router.get("/{hiring_id}", response_model=HiringRequestResponse)
def get_hiring_request(hiring_id: int, db: Session = Depends(get_db)):
    return service.get_hiring_request_by_id(db, hiring_id)


@router.put("/{hiring_id}", response_model=HiringRequestResponse)
def update_hiring(
    hiring_id: int,
    update_data: HiringRequestUpdate,
    db: Session = Depends(get_db)
):
    return service.update_hiring_request(db, hiring_id, update_data)


@router.delete("/{hiring_id}")
def delete_hiring(hiring_id: int, db: Session = Depends(get_db)):
    return service.delete_hiring_request(db, hiring_id)