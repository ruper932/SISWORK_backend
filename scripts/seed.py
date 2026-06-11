from datetime import date

from sqlalchemy import select

from app.db.session import SessionLocal

from app.core.security import hash_password

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


db = SessionLocal()


def seed_roles():

    roles = [
        "CLIENT",
        "PROFESSIONAL",
        "ADMIN",
        "SUPPORT",
        "SUPERADMIN",
    ]

    for role_name in roles:

        existing = db.scalar(
            select(Role).where(
                Role.name == role_name
            )
        )

        if not existing:

            role = Role(
                name=role_name,
            )

            db.add(role)

    db.commit()

    print("Roles seeded")


def seed_superadmin():

    existing = db.scalar(
        select(User).where(
            User.ci == "SUPERADMIN"
        )
    )

    if existing:
        print("Superadmin already exists")
        return

    user = User(
        ci="SUPERADMIN",
        first_name="Super",
        last_name="Admin",
        mother_last_name="System",
        birth_date=date(1990, 1, 1),
        email="superadmin@siswork.com",
        phone="70000000",
        password_hash=hash_password(
            "demons312es"
        ),
        city="La Paz",
        zone="Central",
        is_verified=True,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    role = db.scalar(
        select(Role).where(
            Role.name == "SUPERADMIN"
        )
    )

    user_role = UserRole(
        user_ci=user.ci,
        role_id=role.id,
    )

    db.add(user_role)

    db.commit()

    print("Superadmin seeded")


def seed_client():

    existing = db.scalar(
        select(User).where(
            User.ci == "CLIENT001"
        )
    )

    if existing:
        print("Client already exists")
        return

    user = User(
        ci="CLIENT001",
        first_name="Test",
        last_name="Client",
        mother_last_name="User",
        birth_date=date(1998, 5, 10),
        email="client@siswork.com",
        phone="71111111",
        password_hash=hash_password(
            "demons312es"
        ),
        city="La Paz",
        zone="Sopocachi",
        is_verified=False,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    role = db.scalar(
        select(Role).where(
            Role.name == "CLIENT"
        )
    )

    user_role = UserRole(
        user_ci=user.ci,
        role_id=role.id,
    )

    db.add(user_role)

    db.commit()

    print("Client seeded")


def run_seed():

    print("Starting seed...")

    seed_roles()

    seed_superadmin()

    seed_client()

    print("Seed completed")


if __name__ == "__main__":
    run_seed()