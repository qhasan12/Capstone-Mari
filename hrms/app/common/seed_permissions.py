from sqlalchemy.orm import Session
from app.permissions.models import Permission


DEFAULT_PERMISSIONS = [

    # =========================
    # Departments
    # =========================
    "department:create",
    "department:view",
    "department:update",
    "department:delete",

    # =========================
    # Roles
    # =========================
    "role:create",
    "role:view",
    "role:update",
    "role:delete",

    # =========================
    # Employees
    # =========================
    "employee:create",
    "employee:view",
    "employee:update",
    "employee:delete",
    "employee:view_team",
    "employee:view_self",

    # =========================
    # Hiring Requests
    # =========================
    "hiring_request:create",
    "hiring_request:view",
    "hiring_request:update",
    "hiring_request:delete",

    # =========================
    # Job Postings
    # =========================
    "job_posting:create",
    "job_posting:view",
    "job_posting:update",
    "job_posting:delete",

    # =========================
    # Onboarding
    # =========================
    "onboarding:create",
    "onboarding:view",
    "onboarding:update",
    "onboarding:delete",

    # =========================
    # Training
    # =========================
    "training:create",
    "training:view",
    "training:update",
    "training:delete",

    # =========================
    # Leave Types
    # =========================
    "leave_type:create",
    "leave_type:view",
    "leave_type:update",
    "leave_type:delete",

    # =========================
    # Leave Balances
    # =========================
    "leave_balance:create",
    "leave_balance:view",
    "leave_balance:update",
    "leave_balance:delete",
    "leave_balance:view_team",
    "leave_balance:view_self",

    # =========================
    # Leave Requests
    # =========================
    "leave_request:create",
    "leave_request:view",
    "leave_request:update",
    "leave_request:delete",
    "leave_request:approve",
    "leave_request:view_team",
    "leave_request:view_self",

    # =========================
    # Resignations
    # =========================
    "resignation:create",
    "resignation:view",
    "resignation:update",
    "resignation:delete",
    "resignation:approve",
    "resignation:view_team",
    "resignation:view_self",

    # =========================
    # Clearance
    # =========================
    "clearance:view",
    "clearance:update",
    "clearance:delete",
]


def seed_permissions(db: Session):
    """
    Seed permissions safely (no duplicates).
    """

    for perm_name in DEFAULT_PERMISSIONS:

        existing = db.query(Permission).filter(
            Permission.name == perm_name
        ).first()

        if not existing:
            permission = Permission(name=perm_name)
            db.add(permission)

    db.commit()