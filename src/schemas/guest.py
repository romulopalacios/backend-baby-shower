from pydantic import BaseModel, Field
from typing import Optional

# 1. Esquema Base (Propiedades compartidas)
class GuestBase(BaseModel):
    nombre_mostrar: str = Field(..., description="Nombre visible en la UI")
    cupos_totales: int = Field(..., ge=1, description="Máximo de personas permitidas")

# 2. Esquema para la respuesta de la API (Lo que lee el Frontend)
class GuestResponse(GuestBase):
    id: str
    estado_rsvp: str = Field(default="pendiente", pattern="^(pendiente|confirmado|declinado)$")
    asistentes_confirmados: int = Field(default=0, ge=0)
    restricciones_alimentarias: Optional[str] = None

# 3. Esquema para cuando el invitado confirma (Lo que envía el Frontend)
class GuestUpdate(BaseModel):
    estado_rsvp: str = Field(..., pattern="^(confirmado|declinado)$")
    asistentes_confirmados: int = Field(..., ge=0)
    restricciones_alimentarias: Optional[str] = None