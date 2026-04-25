from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 1. URL completamente limpia (hemos retirado "?ssl=require&channel_binding=require")
DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_ikeBdox1K7yP@ep-twilight-flower-am5rqo4a-pooler.c-5.us-east-1.aws.neon.tech/neondb"

# 2. Motor configurado delegando la seguridad a connect_args
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    connect_args={"ssl": "require"} # <-- La seguridad se maneja internamente aquí
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()