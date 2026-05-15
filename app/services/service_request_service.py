# app/services/service_request_service.py
from datetime import datetime
from fastapi import HTTPException, status

from app.models.enums import ContactChannel, ServiceRequestStatus
from app.models.service_request import ServiceRequest
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.service_request_repository import ServiceRequestRepository
from app.repositories.specialty_repository import SpecialtyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.service_request import ServiceRequestCreateRequest, ServiceRequestUpdateRequest


class ServiceRequestService:
    def __init__(self, db):
        self.repo = ServiceRequestRepository(db)
        self.user_repo = UserRepository(db)
        self.specialty_repo = SpecialtyRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)

    def _validate_budget_range(self, minimum_budget, maximum_budget):
        if minimum_budget is None and maximum_budget is None:
            return
        if minimum_budget is None or maximum_budget is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="minimum_budget and maximum_budget must both be provided",
            )
        if minimum_budget < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="minimum_budget must be greater than or equal to 0",
            )
        if maximum_budget < minimum_budget:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="maximum_budget must be greater than or equal to minimum_budget",
            )

    def _validate_preferred_time_range(self, preferred_start_time, preferred_end_time):
        if preferred_start_time is None and preferred_end_time is None:
            return
        if preferred_start_time is None or preferred_end_time is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="preferred_start_time and preferred_end_time must both be provided",
            )
        if preferred_start_time >= preferred_end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="preferred_start_time must be less than preferred_end_time",
            )

    def _validate_foreign_keys(self, client_user_id=None, specialty_id=None, assigned_professional_profile_id=None):
        if client_user_id is not None:
            user = self.user_repo.get_by_id(client_user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Client user not found",
                )

        if specialty_id is not None:
            specialty = self.specialty_repo.get_by_id(specialty_id)
            if not specialty:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Specialty not found",
                )

        if assigned_professional_profile_id is not None:
            profile = self.profile_repo.get_by_id(assigned_professional_profile_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assigned professional profile not found",
                )

    def _serialize(self, item):
        return {
            "id": item.id,
            "client_user_id": item.client_user_id,
            "specialty_id": item.specialty_id,
            "title": item.title,
            "description": item.description,
            "department": item.department,
            "city": item.city,
            "zone": item.zone,
            "address": item.address,
            "reference": item.reference,
            "preferred_date": item.preferred_date,
            "preferred_start_time": item.preferred_start_time,
            "preferred_end_time": item.preferred_end_time,
            "minimum_budget": item.minimum_budget,
            "maximum_budget": item.maximum_budget,
            "status": item.status.value,
            "assigned_professional_profile_id": item.assigned_professional_profile_id,
            "contact_channel": item.contact_channel.value,
            "is_active": item.is_active,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
            "closed_at": item.closed_at,
        }

    def list_items(self):
        return [self._serialize(item) for item in self.repo.list_items()]

    def list_by_client_user_id(self, client_user_id):
        return [self._serialize(item) for item in self.repo.list_by_client_user_id(client_user_id)]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service request not found",
            )
        return self._serialize(item)

    def create_item(self, payload: ServiceRequestCreateRequest):
        self._validate_foreign_keys(
            client_user_id=payload.client_user_id,
            specialty_id=payload.specialty_id,
            assigned_professional_profile_id=payload.assigned_professional_profile_id,
        )
        self._validate_budget_range(payload.minimum_budget, payload.maximum_budget)
        self._validate_preferred_time_range(payload.preferred_start_time, payload.preferred_end_time)

        item = ServiceRequest(
            client_user_id=payload.client_user_id,
            specialty_id=payload.specialty_id,
            title=payload.title,
            description=payload.description,
            department=payload.department,
            city=payload.city,
            zone=payload.zone,
            address=payload.address,
            reference=payload.reference,
            preferred_date=payload.preferred_date,
            preferred_start_time=payload.preferred_start_time,
            preferred_end_time=payload.preferred_end_time,
            minimum_budget=payload.minimum_budget,
            maximum_budget=payload.maximum_budget,
            status=ServiceRequestStatus.OPEN,
            assigned_professional_profile_id=payload.assigned_professional_profile_id,
            contact_channel=ContactChannel(payload.contact_channel),
            is_active=payload.is_active,
        )

        created = self.repo.create(item)
        return self._serialize(created)

    def update_item(self, item_id, payload: ServiceRequestUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service request not found",
            )

        data = payload.model_dump(exclude_unset=True)

        if "specialty_id" in data:
            self._validate_foreign_keys(specialty_id=data["specialty_id"])

        if "assigned_professional_profile_id" in data and data["assigned_professional_profile_id"] is not None:
            self._validate_foreign_keys(assigned_professional_profile_id=data["assigned_professional_profile_id"])

        next_minimum_budget = data.get("minimum_budget", item.minimum_budget)
        next_maximum_budget = data.get("maximum_budget", item.maximum_budget)
        self._validate_budget_range(next_minimum_budget, next_maximum_budget)

        next_preferred_start_time = data.get("preferred_start_time", item.preferred_start_time)
        next_preferred_end_time = data.get("preferred_end_time", item.preferred_end_time)
        self._validate_preferred_time_range(next_preferred_start_time, next_preferred_end_time)

        if "specialty_id" in data:
            item.specialty_id = data["specialty_id"]
        if "title" in data:
            item.title = data["title"]
        if "description" in data:
            item.description = data["description"]
        if "department" in data:
            item.department = data["department"]
        if "city" in data:
            item.city = data["city"]
        if "zone" in data:
            item.zone = data["zone"]
        if "address" in data:
            item.address = data["address"]
        if "reference" in data:
            item.reference = data["reference"]
        if "preferred_date" in data:
            item.preferred_date = data["preferred_date"]
        if "preferred_start_time" in data:
            item.preferred_start_time = data["preferred_start_time"]
        if "preferred_end_time" in data:
            item.preferred_end_time = data["preferred_end_time"]
        if "minimum_budget" in data:
            item.minimum_budget = data["minimum_budget"]
        if "maximum_budget" in data:
            item.maximum_budget = data["maximum_budget"]
        if "status" in data:
            item.status = ServiceRequestStatus(data["status"])
        if "assigned_professional_profile_id" in data:
            item.assigned_professional_profile_id = data["assigned_professional_profile_id"]
        if "contact_channel" in data:
            item.contact_channel = ContactChannel(data["contact_channel"])
        if "is_active" in data:
            item.is_active = data["is_active"]
        if "closed_at" in data:
            item.closed_at = data["closed_at"]

        updated = self.repo.save(item)
        return self._serialize(updated)

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service request not found",
            )

        self.repo.delete(item)
        return {"message": "Service request deleted successfully"}