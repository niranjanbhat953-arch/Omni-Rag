from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routes_auth import router as auth_router
from .routes_documents import router as documents_router
from .routes_research import router as research_router
from .routes_users import router as users_router
from .settings import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title=settings.app_name, version='0.2.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[item.strip() for item in settings.cors_origins.split(',')], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(research_router)
app.include_router(users_router)

@app.get('/health', tags=['system'])
async def health() -> dict[str, str]:
    return {'status': 'ok', 'service': settings.app_name}
