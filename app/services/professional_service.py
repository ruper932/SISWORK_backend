from __future__ import annotations

import os
import uuid
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy import select

from app.models.file import File
from app.models.professional_profile import ProfessionalProfile
from app.models.professional_specialty import ProfessionalSpecialty
from app.models.specialty import Specialty
from app.models.user import User
from app.models.verification_document import VerificationDocument
from app.models.verification_request import VerificationRequest
from app.repositories.professional_repository import ProfessionalRepository
from app.schemas.professional import ProfessionalPublicResponse
from app.db.enums import VerificationStatusEnum, VerificationDocumentTypeEnum

UPLOAD_DIR = "uploads/verification"


class ProfessionalService:
    @staticmethod
    async def request_verification(db, current_user, ci_photo: UploadFile, selfie_photo: UploadFile, certificate_pdf: UploadFile):
        existing_profile = db.scalar(
            select(ProfessionalProfile).where(ProfessionalProfile.user_ci == current_user.ci)
        )

        if not existing_profile:
            profile = ProfessionalProfile(
                user_ci=current_user.ci,
                verification_status=VerificationStatusEnum.PENDING,
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        else:
            profile = existing_profile

        verification_request = VerificationRequest(
            professional_profile_id=profile.id,
            status=VerificationStatusEnum.PENDING,
        )
        db.add(verification_request)
        db.commit()
        db.refresh(verification_request)

        files_data = [
            (ci_photo, VerificationDocumentTypeEnum.ID_CARD_FRONT),
            (selfie_photo, VerificationDocumentTypeEnum.SELFIE),
            (certificate_pdf, VerificationDocumentTypeEnum.PDF_CERTIFICATION),
        ]

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        for upload_file, doc_type in files_data:
            extension = upload_file.filename.split(".")[-1]
            generated_name = f"{uuid.uuid4()}.{extension}"
            file_path = os.path.join(UPLOAD_DIR, generated_name)

            content = await upload_file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(content)

            file_record = File(
                uploaded_by_ci=current_user.ci,
                original_filename=upload_file.filename,
                stored_filename=generated_name,
                file_path=file_path,
                mimetype=upload_file.content_type,
                file_size=len(content),
            )
            db.add(file_record)
            db.commit()
            db.refresh(file_record)

            verification_document = VerificationDocument(
                verification_request_id=verification_request.id,
                file_id=file_record.id,
                document_type=doc_type,
            )
            db.add(verification_document)
            db.commit()

        return verification_request

    @staticmethod
    def search_public_professionals(
        db,
        q: Optional[str] = None,
        specialty_id: Optional[uuid.UUID] = None,
        city: Optional[str] = None,
        zone: Optional[str] = None,
        min_rating: Optional[float] = None,
        is_available: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ):
        profiles = ProfessionalRepository.search_public_professionals(
            db=db,
            q=q,
            specialty_id=specialty_id,
            city=city,
            zone=zone,
            min_rating=min_rating,
            is_available=is_available,
            skip=skip,
            limit=limit,
        )

        results = []
        for profile in profiles:
            full_name_parts = [
                profile.user.first_name,
                profile.user.last_name,
                profile.user.mother_last_name,
            ]
            full_name = " ".join([part for part in full_name_parts if part])

            specialties = []
            for item in profile.specialties:
                if item.specialty:
                    specialties.append(
                        {
                            "id": item.specialty.id,
                            "name": item.specialty.name,
                            "description": item.specialty.description,
                        }
                    )

            availabilities = []
            for item in profile.availabilities:
                availabilities.append(
                    {
                        "id": item.id,
                        "day_of_week": item.day_of_week,
                        "start_time": item.start_time,
                        "end_time": item.end_time,
                        "is_active": item.is_active,
                    }
                )

            results.append(
                {
                    "id": profile.id,
                    "user_ci": profile.user_ci,
                    "full_name": full_name,
                    "bio": profile.bio,
                    "experience_years": profile.experience_years,
                    "verification_status": profile.verification_status,
                    "rating_average": profile.rating_average,
                    "rating_count": profile.rating_count,
                    "is_available": profile.is_available,
                    "city": profile.user.city,
                    "zone": profile.user.zone,
                    "specialties": specialties,
                    "availabilities": availabilities,
                }
            )

        return results


    @staticmethod
    def get_public_professional_detail(db, user_ci: str):
        profile = ProfessionalRepository.get_by_user_ci(db, user_ci)
        if not profile:
            raise Exception("Professional profile not found")

        if profile.verification_status != VerificationStatusEnum.APPROVED:
            raise Exception("Professional profile is not public")

        full_name_parts = [
            profile.user.first_name,
            profile.user.last_name,
            profile.user.mother_last_name,
        ]
        full_name = " ".join([part for part in full_name_parts if part])

        specialties = []
        for item in profile.specialties:
            if item.specialty:
                specialties.append(
                    {
                        "id": item.specialty.id,
                        "name": item.specialty.name,
                        "description": item.specialty.description,
                    }
                )

        availabilities = []
        for item in profile.availabilities:
            availabilities.append(
                {
                    "id": item.id,
                    "day_of_week": item.day_of_week,
                    "start_time": item.start_time,
                    "end_time": item.end_time,
                    "is_active": item.is_active,
                }
            )

        return {
            "id": profile.id,
            "user_ci": profile.user_ci,
            "full_name": full_name,
            "bio": profile.bio,
            "experience_years": profile.experience_years,
            "verification_status": profile.verification_status,
            "rating_average": profile.rating_average,
            "rating_count": profile.rating_count,
            "is_available": profile.is_available,
            "city": profile.user.city,
            "zone": profile.user.zone,
            "specialties": specialties,
            "availabilities": availabilities,
        }