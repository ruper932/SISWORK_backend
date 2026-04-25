import enum


class UserRole(str, enum.Enum):
    CLIENT = "CLIENT"
    PROFESSIONAL = "PROFESSIONAL"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"


class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


class UserGender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY"