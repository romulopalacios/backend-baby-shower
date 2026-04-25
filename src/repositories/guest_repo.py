import json
from pathlib import Path
from typing import List, Optional
from src.schemas.guest import GuestResponse, GuestUpdate

class JSONGuestRepository:
    def __init__(self, file_path: str = "data/master_guest_list.json"):
        self.file_path = Path(file_path)
        # Nos aseguramos de que el directorio y el archivo existan al instanciar
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f) # Inicializamos con una lista vacía

    # Métodos privados de lectura/escritura (I/O)
    def _read_data(self) -> List[dict]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_data(self, data: List[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # Métodos Asíncronos Públicos (Lo que consumirá FastAPI)
    
    async def get_all_guests(self) -> List[GuestResponse]:
        """Obtiene la lista completa de invitados."""
        data = self._read_data()
        return [GuestResponse(**item) for item in data]

    async def get_guest_by_id(self, guest_id: str) -> Optional[GuestResponse]:
        """Busca un invitado específico por su ID único."""
        data = self._read_data()
        for item in data:
            if item["id"] == guest_id:
                return GuestResponse(**item)
        return None

    async def update_rsvp(self, guest_id: str, update_data: GuestUpdate) -> Optional[GuestResponse]:
        """Actualiza el estado de confirmación de un invitado."""
        data = self._read_data()
        for item in data:
            if item["id"] == guest_id:
                # Validamos reglas de negocio: no pueden ir más de los cupos totales
                if update_data.asistentes_confirmados > item["cupos_totales"]:
                    raise ValueError(f"No puedes confirmar más de {item['cupos_totales']} cupos.")
                
                # Actualizamos los campos
                item["estado_rsvp"] = update_data.estado_rsvp
                item["asistentes_confirmados"] = update_data.asistentes_confirmados
                
                if update_data.restricciones_alimentarias is not None:
                    item["restricciones_alimentarias"] = update_data.restricciones_alimentarias
                
                # Guardamos en el "disco"
                self._write_data(data)
                return GuestResponse(**item)
        
        return None # Retorna None si el ID no existe