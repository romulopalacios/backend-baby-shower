from sqlalchemy import Column, String, Integer
from src.db.database import Base

class GuestModel(Base):
    __tablename__ = "guests"

    id = Column(String, primary_key=True, index=True)
    nombre_mostrar = Column(String, nullable=False)
    cupos_totales = Column(Integer, nullable=False)
    estado_rsvp = Column(String, default="pendiente")
    asistentes_confirmados = Column(Integer, default=0)
    restricciones_alimentarias = Column(String, nullable=True)