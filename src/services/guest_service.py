from typing import List, Optional
from src.repositories.guest_repo import JSONGuestRepository
from src.schemas.guest import GuestResponse, GuestUpdate
from fastapi import HTTPException

class GuestService:
    def __init__(self, repository: JSONGuestRepository):
        self.repository = repository

    async def get_invitation_details(self, guest_id: str) -> GuestResponse:
        guest = await self.repository.get_guest_by_id(guest_id)
        if not guest:
            raise HTTPException(status_code=404, detail="Invitación no encontrada.")
        return guest

    async def process_rsvp(self, guest_id: str, update_data: GuestUpdate) -> GuestResponse:
        try:
            updated_guest = await self.repository.update_rsvp(guest_id, update_data)
            if not updated_guest:
                raise HTTPException(status_code=404, detail="Invitado no existe.")
            return updated_guest
        except ValueError as e:
            # Capturamos la validación de cupos que hicimos en el repo
            raise HTTPException(status_code=400, detail=str(e))