from sqlalchemy.orm import Session
from app.roles.models import Role
from app.permissions.models import Permission, RolePermission


ROLE_PERMISSION_MAP = {

    # =========================
    # SuperAdmin (all permissions)
    # =========================
    "SA": "*",

    # =========================
    # HR
    # =========================
    "HR": [

        # Employees
        "employee:create",
        "employee:view",
        "employee:update",
        "employee:delete",

        # Departments
        "department:view",

        # Hiring
        "hiring_request:create",
        "hiring_request:view",
        "hiring_request:update",
        "hiring_request:delete",

        # Job postings
        "job_posting:create",
        "job_posting:view",
        "job_posting:update",
        "job_posting:delete",

        # Onboarding
        "onboarding:create",
        "onboarding:view",
        "onboarding:update",
        "onboarding:delete",

        # Training
        "training:create",
        "training:view",
        "training:update",
        "training:delete",

        # Leave types
        "leave_type:create",
        "leave_type:view",
        "leave_type:update",
        "leave_type:delete",
        

        # Leave balances
        "leave_balance:create",
        "leave_balance:view",
        "leave_balance:update",
        "leave_balance:delete",
        "leave_balance:view_team",
        "leave_balance:view_self",
      

        # Leave requests
        "leave_request:update",
        "leave_request:create",
        "leave_request:view",
        "leave_request:approve",
        "leave_request:reject",
        "leave_request:delete",
        "leave_request:cancel",

        # Resignations
        "resignation:view",
        "resignation:approve",
        "resignation:reject",
        "resignation:create",
        "resignation:update",
        "resignation:delete",
        

        # Clearance
        "clearance:view",
        "clearance:update",
        "clearance:delete",
    ],

    # =========================
    # Manager
    # =========================
    "MGR": [

        "employee:view_team",
        "leave_request:create",
        "leave_request:view_team",
        "leave_request:approve",
        "leave_request:reject",
        "leave_request:cancel",

        "leave_balance:view_team",
        "training:view_team",
        
        

        "resignation:view_team",
        "resignation:create",
        "resignation:approve",
        "resignation:reject",
        
        "job_posting:view",
        "department:view",
        "leave_type:view",
    ],

    # =========================
    # Employee
    # =========================
    "EMP": [

        "employee:view_self",
        "employee:update_self",

        "leave_request:create",
        "leave_request:view_self",
        "leave_request:update",
        "leave_request:cancel",

        "leave_balance:view_self",

        "resignation:create",
        "resignation:view_self",
        "resignation:withdraw",

        "training:view_self",
        "job_posting:view",
        "leave_type:view",
        "department:view",
    ]
}


def seed_role_permissions(db: Session):

    roles = db.query(Role).all()
    permissions = db.query(Permission).all()

    perm_map = {p.name: p.id for p in permissions}

    existing = {
        (rp.role_id, rp.permission_id)
        for rp in db.query(RolePermission).all()
    }

    new_assignments = []

    for role in roles:

        role_perms = ROLE_PERMISSION_MAP.get(role.title)

        if not role_perms:
            continue

        # SuperAdmin → all permissions
        if role_perms == "*":
            role_perms = perm_map.keys()

        for perm_name in role_perms:

            perm_id = perm_map.get(perm_name)

            if not perm_id:
                continue

            if (role.id, perm_id) not in existing:
                new_assignments.append(
                    RolePermission(
                        role_id=role.id,
                        permission_id=perm_id
                    )
                )

    if new_assignments:
        db.add_all(new_assignments)
        db.commit()

    print(f"{len(new_assignments)} role-permissions seeded.")