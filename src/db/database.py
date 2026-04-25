import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 1. Intentamos leer la variable de entorno de Render. 
# Si no existe (en tu local), usamos la URL que ya tenemos.
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://neondb_owner:npg_ikeBdox1K7yP@ep-twilight-flower-am5rqo4a-pooler.c-5.us-east-1.aws.neon.tech/neondb"
)

# Render a veces entrega la URL como 'postgres://'. 
# SQLAlchemy asíncrono EXIGE que empiece con 'postgresql+asyncpg://'.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 2. Configuración del motor con SSL forzado para Neon
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"ssl": "require"}
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()