from fastapi import HTTPException


def ensure_superadmin(current_user):

    if (
        not current_user.employee
        or not current_user.employee.role
        or current_user.employee.role.title != "SA"
    ):
        raise HTTPException(
            status_code=403,
            detail="Only SuperAdmin is allowed to perform this action"
        )