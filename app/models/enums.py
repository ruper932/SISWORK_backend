import enum


class UserRole(str, enum.Enum):
    CLIENT = "client"
    PROFESSIONAL = "professional"
    ADMIN = "admin"
    SUPPORT = "support"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BLOCKED = "blocked"
    DELETED = "deleted"