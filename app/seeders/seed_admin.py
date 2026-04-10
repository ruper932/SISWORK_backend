from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_admin(db: Session) -> dict:
    email = "admin@siswork.com"

    existing = db.query(User).filter(User.correo == email).first()
    if existing:
        return {
            "created": False,
            "email": email,
            "detail": "El usuario admin ya existe"
        }

    admin = User(
        nombres="Admin",
        apellidos="SISWORK",
        correo=email,
        contrasena_hash=pwd_context.hash("Admin123*"),
        telefono="70000000",
        numero_whatsapp="70000000",
        rol="administrador",
        estado="activo",
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {
        "created": True,
        "email": email,
        "detail": "Usuario admin creado correctamente"
    }