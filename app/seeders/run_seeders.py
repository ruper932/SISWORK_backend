from sqlalchemy.orm import Session

from app.seeders.seed_admin import seed_admin


def run_seeders(db: Session) -> dict:
    admin_result = seed_admin(db)

    return {
        "ok": True,
        "results": {
            "admin": admin_result
        }
    }