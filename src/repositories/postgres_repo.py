from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.guest import GuestModel
from src.schemas.guest import GuestResponse, GuestUpdate
from typing import List, Optional

class PostgresGuestRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_guest_by_id(self, guest_id: str) -> Optional[GuestResponse]:
        result = await self.db.execute(select(GuestModel).filter(GuestModel.id == guest_id))
        guest = result.scalars().first()
        
        if guest:
            # Convertimos el modelo de base de datos a nuestro esquema Pydantic
            return GuestResponse(
                id=guest.id,
                nombre_mostrar=guest.nombre_mostrar,
                cupos_totales=guest.cupos_totales,
                estado_rsvp=guest.estado_rsvp,
                asistentes_confirmados=guest.asistentes_confirmados,
                restricciones_alimentarias=guest.restricciones_alimentarias
            )
        return None

    async def update_rsvp(self, guest_id: str, update_data: GuestUpdate) -> Optional[GuestResponse]:
        result = await self.db.execute(select(GuestModel).filter(GuestModel.id == guest_id))
        guest = result.scalars().first()

        if guest:
            if update_data.asistentes_confirmados > guest.cupos_totales:
                raise ValueError(f"No puedes confirmar más de {guest.cupos_totales} cupos.")

            guest.estado_rsvp = update_data.estado_rsvp
            guest.asistentes_confirmados = update_data.asistentes_confirmados
            if update_data.restricciones_alimentarias is not None:
                guest.restricciones_alimentarias = update_data.restricciones_alimentarias

            await self.db.commit()
            await self.db.refresh(guest)
            
            return await self.get_guest_by_id(guest_id)
        
        return None