# app/services/professional_profile_service.py
from fastapi import HTTPException, status

from app.models.enums import VerificationStatus
from app.models.professional_profile import ProfessionalProfile
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.user_repository import UserRepository
from app.schemas.professional_profile import (
    ProfessionalProfileCreateRequest,
    ProfessionalProfileUpdateRequest,
)


class ProfessionalProfileService:
    def __init__(self, db):
        self.repo = ProfessionalProfileRepository(db)
        self.user_repo = UserRepository(db)

    def list_profiles(self):
        profiles = self.repo.list_profiles()

        return [
            {
                "id": profile.id,
                "user_id": profile.user_id,
                "bio": profile.bio,
                "years_experience": profile.years_experience,
                "main_zone": profile.main_zone,
                "service_radius_km": profile.service_radius_km,
                "verification_status": profile.verification_status.value,
                "average_rating": profile.average_rating,
                "ratings_count": profile.ratings_count,
                "completed_services_count": profile.completed_services_count,
                "available_now": profile.available_now,
                "public_contact_enabled": profile.public_contact_enabled,
                "created_at": profile.created_at,
            }
            for profile in profiles
        ]

    def get_profile(self, profile_id):
        profile = self.repo.get_by_id(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional profile not found",
            )

        return {
            "id": profile.id,
            "user_id": profile.user_id,
            "bio": profile.bio,
            "years_experience": profile.years_experience,
            "main_zone": profile.main_zone,
            "service_radius_km": profile.service_radius_km,
            "work_reference": profile.work_reference,
            "identity_document_url": profile.identity_document_url,
            "verification_status": profile.verification_status.value,
            "verification_requested_at": profile.verification_requested_at,
            "verification_resolved_at": profile.verification_resolved_at,
            "verified_by_user_id": profile.verified_by_user_id,
            "average_rating": profile.average_rating,
            "ratings_count": profile.ratings_count,
            "completed_services_count": profile.completed_services_count,
            "available_now": profile.available_now,
            "public_contact_enabled": profile.public_contact_enabled,
            "created_at": profile.created_at,
            "updated_at": profile.updated_at,
        }

    def create_profile(self, payload: ProfessionalProfileCreateRequest):
        user = self.user_repo.get_by_id(payload.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        existing_profile = self.repo.get_by_user_id(payload.user_id)
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already has a professional profile",
            )

        profile = ProfessionalProfile(
            user_id=payload.user_id,
            bio=payload.bio,
            years_experience=payload.years_experience,
            main_zone=payload.main_zone,
            service_radius_km=payload.service_radius_km,
            work_reference=payload.work_reference,
            identity_document_url=payload.identity_document_url,
            verification_status=VerificationStatus(payload.verification_status),
            available_now=payload.available_now,
            public_contact_enabled=payload.public_contact_enabled,
        )

        created = self.repo.create(profile)

        return {
            "id": created.id,
            "user_id": created.user_id,
            "bio": created.bio,
            "years_experience": created.years_experience,
            "main_zone": created.main_zone,
            "service_radius_km": created.service_radius_km,
            "verification_status": created.verification_status.value,
            "available_now": created.available_now,
            "public_contact_enabled": created.public_contact_enabled,
            "created_at": created.created_at,
        }

    def update_profile(self, profile_id, payload: ProfessionalProfileUpdateRequest):
        profile = self.repo.get_by_id(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional profile not found",
            )

        data = payload.model_dump(exclude_unset=True)

        if "bio" in data:
            profile.bio = data["bio"]
        if "years_experience" in data:
            profile.years_experience = data["years_experience"]
        if "main_zone" in data:
            profile.main_zone = data["main_zone"]
        if "service_radius_km" in data:
            profile.service_radius_km = data["service_radius_km"]
        if "work_reference" in data:
            profile.work_reference = data["work_reference"]
        if "identity_document_url" in data:
            profile.identity_document_url = data["identity_document_url"]
        if "verification_status" in data:
            profile.verification_status = VerificationStatus(data["verification_status"])
        if "verification_requested_at" in data:
            profile.verification_requested_at = data["verification_requested_at"]
        if "verification_resolved_at" in data:
            profile.verification_resolved_at = data["verification_resolved_at"]
        if "verified_by_user_id" in data:
            profile.verified_by_user_id = data["verified_by_user_id"]
        if "available_now" in data:
            profile.available_now = data["available_now"]
        if "public_contact_enabled" in data:
            profile.public_contact_enabled = data["public_contact_enabled"]

        updated = self.repo.save(profile)

        return {
            "id": updated.id,
            "user_id": updated.user_id,
            "bio": updated.bio,
            "years_experience": updated.years_experience,
            "main_zone": updated.main_zone,
            "service_radius_km": updated.service_radius_km,
            "work_reference": updated.work_reference,
            "identity_document_url": updated.identity_document_url,
            "verification_status": updated.verification_status.value,
            "verification_requested_at": updated.verification_requested_at,
            "verification_resolved_at": updated.verification_resolved_at,
            "verified_by_user_id": updated.verified_by_user_id,
            "average_rating": updated.average_rating,
            "ratings_count": updated.ratings_count,
            "completed_services_count": updated.completed_services_count,
            "available_now": updated.available_now,
            "public_contact_enabled": updated.public_contact_enabled,
            "created_at": updated.created_at,
            "updated_at": updated.updated_at,
        }

    def delete_profile(self, profile_id):
        profile = self.repo.get_by_id(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional profile not found",
            )

        self.repo.delete(profile)
        return {"message": "Professional profile deleted successfully"}