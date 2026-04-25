from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importamos nuestros esquemas, configuración de BD, repo y servicio
from src.schemas.guest import GuestResponse, GuestUpdate
from src.db.database import engine, Base, AsyncSessionLocal
from src.repositories.postgres_repo import PostgresGuestRepository
from src.services.guest_service import GuestService

# 1. Ciclo de vida de la aplicación (Crea las tablas al arrancar)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al encender: Nos conectamos a Neon y creamos la tabla si no existe
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Al apagar: Cerramos las conexiones limpiamente
    await engine.dispose()

# 2. Inicialización de FastAPI
app = FastAPI(
    title="Leo's Baby Shower API",
    description="Backend robusto conectado a Neon Serverless PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

# 3. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambia esto a tu dominio de Vercel
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 4. Inyección de Dependencias
async def get_db():
    """Genera una sesión de BD asíncrona por cada petición web"""
    async with AsyncSessionLocal() as session:
        yield session

def get_guest_service(db = Depends(get_db)):
    """Inyecta la sesión de la BD en el repositorio y luego en el servicio"""
    repo = PostgresGuestRepository(db)
    return GuestService(repo)

# 5. Endpoints
@app.get("/guests/{guest_id}", response_model=GuestResponse)
async def get_guest(guest_id: str, service: GuestService = Depends(get_guest_service)):
    """Obtiene los detalles personalizados de un invitado"""
    return await service.get_invitation_details(guest_id)

@app.post("/guests/{guest_id}/rsvp", response_model=GuestResponse)
async def update_rsvp(
    guest_id: str, 
    update_data: GuestUpdate, 
    service: GuestService = Depends(get_guest_service)
):
    """Procesa la confirmación de asistencia"""
    return await service.process_rsvp(guest_id, update_data)

@app.get("/health")
async def health_check():
    """Endpoint de monitoreo"""
    return {"status": "online", "database": "Neon PostgreSQL"}