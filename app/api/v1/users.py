from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    roles = [user_role.role.name for user_role in current_user.user_roles]

    return {
        "ci": current_user.ci,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "mother_last_name": current_user.mother_last_name,
        "birth_date": current_user.birth_date,
        "email": current_user.email,
        "phone": current_user.phone,
        "city": current_user.city,
        "zone": current_user.zone,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "roles": roles,
    }


@router.get(
    "",
    response_model=UserListResponse,
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "SUPERADMIN"])),
    q: str | None = Query(default=None),
    role: str | None = Query(default=None),
    city: str | None = Query(default=None),
    zone: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    is_verified: bool | None = Query(default=None),
    include_deleted: bool = Query(default=False),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
):
    try:
        return UserService.list_users(
            db=db,
            q=q,
            role=role,
            city=city,
            zone=zone,
            is_active=is_active,
            is_verified=is_verified,
            include_deleted=include_deleted,
            skip=skip,
            limit=limit,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{ci}",
    response_model=UserResponse,
)
def get_user(
    ci: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "SUPERADMIN"])),
):
    try:
        return UserService.get_user_by_ci(db, ci)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "SUPERADMIN"])),
):
    try:
        return UserService.create_user_admin(db, user_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/{ci}",
    response_model=UserResponse,
)
def update_user(
    ci: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "SUPERADMIN"])),
):
    try:
        return UserService.update_user(db, ci, user_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{ci}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    ci: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "SUPERADMIN"])),
):
    try:
        UserService.delete_user(db, ci)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/{ci}/restore",
    response_model=UserResponse,
)
def restore_user(
    ci: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "SUPERADMIN"])),
):
    try:
        return UserService.restore_user(db, ci)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )