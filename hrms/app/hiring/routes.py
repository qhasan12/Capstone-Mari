from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.schemas import APIResponse
from app.core.database import get_db
from app.auth.security import get_current_user

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
# Job Posting Routes
# =====================================================

@router.post("/job-posting")
def create_job_posting(
    job_data: JobPostingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    posting = service.create_job_posting(db, job_data, current_user)

    return APIResponse(
        code=201,
        message="Job posting created successfully",
        data=JobPostingResponse.model_validate(posting)
    )


@router.get("/job-posting")
def get_job_postings(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    postings = service.get_all_job_postings(db, current_user)

    return APIResponse(
        code=200,
        message="Job postings fetched successfully",
        data=[JobPostingResponse.model_validate(p) for p in postings]
    )


@router.get("/job-posting/{posting_id}")
def get_job_posting(
    posting_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    posting = service.get_job_posting_by_id(db, posting_id, current_user)

    return APIResponse(
        code=200,
        message="Job posting fetched successfully",
        data=JobPostingResponse.model_validate(posting)
    )


@router.patch("/job-posting/{posting_id}")
def update_job_posting(
    posting_id: int,
    update_data: JobPostingUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    posting = service.update_job_posting(db, posting_id, update_data, current_user)

    return APIResponse(
        code=200,
        message="Job posting updated successfully",
        data=JobPostingResponse.model_validate(posting)
    )


@router.delete("/job-posting/{posting_id}")
def delete_job_posting(
    posting_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service.delete_job_posting(db, posting_id, current_user)

    return APIResponse(
        code=200,
        message="Job posting deactivated successfully"
    )


# =====================================================
# Hiring Request Routes
# =====================================================

@router.post("/")
def create_hiring_request(
    hiring_data: HiringRequestCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    hiring = service.create_hiring_request(db, hiring_data, current_user)

    return APIResponse(
        code=201,
        message="Hiring request created successfully",
        data=HiringRequestResponse.model_validate(hiring)
    )


@router.get("/")
def get_hiring_requests(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    hirings = service.get_all_hiring_requests(db, current_user)

    return APIResponse(
        code=200,
        message="Hiring requests fetched successfully",
        data=[HiringRequestResponse.model_validate(h) for h in hirings]
    )


@router.get("/{hiring_id}")
def get_hiring_request(
    hiring_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    hiring = service.get_hiring_request_by_id(db, hiring_id, current_user)

    return APIResponse(
        code=200,
        message="Hiring request fetched successfully",
        data=HiringRequestResponse.model_validate(hiring)
    )


@router.patch("/{hiring_id}")
def update_hiring(
    hiring_id: int,
    update_data: HiringRequestUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    hiring = service.update_hiring_request(db, hiring_id, update_data, current_user)

    return APIResponse(
        code=200,
        message="Hiring request updated successfully",
        data=HiringRequestResponse.model_validate(hiring)
    )


@router.delete("/{hiring_id}")
def delete_hiring(
    hiring_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service.delete_hiring_request(db, hiring_id, current_user)

    return APIResponse(
        code=200,
        message="Hiring request deactivated successfully"
    )