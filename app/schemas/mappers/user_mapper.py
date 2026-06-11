from app.models.user import User
from app.schemas.user import UserResponse


def build_user_response(user: User) -> UserResponse:
    return UserResponse(
        ci=user.ci,
        first_name=user.first_name,
        last_name=user.last_name,
        mother_last_name=user.mother_last_name,
        birth_date=user.birth_date,
        email=user.email,
        phone=user.phone,
        city=user.city,
        zone=user.zone,
        is_active=user.is_active,
        is_verified=user.is_verified,
        roles=[
            user_role.role.name
            for user_role in user.user_roles
            if user_role.role is not None
        ],
    )