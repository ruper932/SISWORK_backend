# app/services/certification_service.py
from datetime import datetime
from fastapi import HTTPException, status

from app.models.certification import Certification
from app.models.enums import DocumentType
from app.repositories.certification_repository import CertificationRepository
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.user_repository import UserRepository
from app.schemas.certification import CertificationCreateRequest, CertificationUpdateRequest


class CertificationService:
    def __init__(self, db):
        self.repo = CertificationRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)
        self.user_repo = UserRepository(db)

    def _validate_issue_year(self, issue_year: int | None):
        if issue_year is None:
            return
        current_year_plus_one = datetime.now().year + 1
        if issue_year < 1950 or issue_year > current_year_plus_one:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="issue_year must be between 1950 and current year + 1",
            )

    def list_items(self):
        items = self.repo.list_items()
        return [
            {
                "id": item.id,
                "professional_profile_id": item.professional_profile_id,
                "document_type": item.document_type.value,
                "title": item.title,
                "institution": item.institution,
                "issue_year": item.issue_year,
                "file_url": item.file_url,
                "is_verified": item.is_verified,
                "verified_by_user_id": item.verified_by_user_id,
                "verified_at": item.verified_at,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]

    def list_by_profile_id(self, profile_id):
        items = self.repo.list_by_profile_id(profile_id)
        return [
            {
                "id": item.id,
                "professional_profile_id": item.professional_profile_id,
                "document_type": item.document_type.value,
                "title": item.title,
                "institution": item.institution,
                "issue_year": item.issue_year,
                "file_url": item.file_url,
                "is_verified": item.is_verified,
                "verified_by_user_id": item.verified_by_user_id,
                "verified_at": item.verified_at,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certification not found",
            )

        return {
            "id": item.id,
            "professional_profile_id": item.professional_profile_id,
            "document_type": item.document_type.value,
            "title": item.title,
            "institution": item.institution,
            "issue_year": item.issue_year,
            "file_url": item.file_url,
            "is_verified": item.is_verified,
            "verified_by_user_id": item.verified_by_user_id,
            "verified_at": item.verified_at,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }

    def create_item(self, payload: CertificationCreateRequest):
        profile = self.profile_repo.get_by_id(payload.professional_profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional profile not found",
            )

        self._validate_issue_year(payload.issue_year)

        item = Certification(
            professional_profile_id=payload.professional_profile_id,
            document_type=DocumentType(payload.document_type),
            title=payload.title,
            institution=payload.institution,
            issue_year=payload.issue_year,
            file_url=payload.file_url,
        )

        created = self.repo.create(item)

        return {
            "id": created.id,
            "professional_profile_id": created.professional_profile_id,
            "document_type": created.document_type.value,
            "title": created.title,
            "institution": created.institution,
            "issue_year": created.issue_year,
            "file_url": created.file_url,
            "is_verified": created.is_verified,
            "verified_by_user_id": created.verified_by_user_id,
            "verified_at": created.verified_at,
            "created_at": created.created_at,
            "updated_at": created.updated_at,
        }

    def update_item(self, item_id, payload: CertificationUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certification not found",
            )

        data = payload.model_dump(exclude_unset=True)

        if "issue_year" in data:
            self._validate_issue_year(data["issue_year"])

        if "verified_by_user_id" in data and data["verified_by_user_id"] is not None:
            user = self.user_repo.get_by_id(data["verified_by_user_id"])
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Verified by user not found",
                )

        if "document_type" in data:
            item.document_type = DocumentType(data["document_type"])
        if "title" in data:
            item.title = data["title"]
        if "institution" in data:
            item.institution = data["institution"]
        if "issue_year" in data:
            item.issue_year = data["issue_year"]
        if "file_url" in data:
            item.file_url = data["file_url"]
        if "is_verified" in data:
            item.is_verified = data["is_verified"]
        if "verified_by_user_id" in data:
            item.verified_by_user_id = data["verified_by_user_id"]
        if "verified_at" in data:
            item.verified_at = data["verified_at"]

        updated = self.repo.save(item)

        return {
            "id": updated.id,
            "professional_profile_id": updated.professional_profile_id,
            "document_type": updated.document_type.value,
            "title": updated.title,
            "institution": updated.institution,
            "issue_year": updated.issue_year,
            "file_url": updated.file_url,
            "is_verified": updated.is_verified,
            "verified_by_user_id": updated.verified_by_user_id,
            "verified_at": updated.verified_at,
            "created_at": updated.created_at,
            "updated_at": updated.updated_at,
        }

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certification not found",
            )

        self.repo.delete(item)
        return {"message": "Certification deleted successfully"}