import enum


class RoleEnum(str, enum.Enum):
    CLIENT = "CLIENT"
    PROFESSIONAL = "PROFESSIONAL"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    SUPERADMIN = "SUPERADMIN"


class VerificationStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class VerificationDocumentTypeEnum(str, enum.Enum):
    ID_CARD_FRONT = "ID_CARD_FRONT"
    ID_CARD_BACK = "ID_CARD_BACK"
    SELFIE = "SELFIE"
    CERTIFICATE = "CERTIFICATE"
    PDF_CERTIFICATION = "PDF_CERTIFICATION"


class RequestStatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class ApplicationStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class UrgencyLevelEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"