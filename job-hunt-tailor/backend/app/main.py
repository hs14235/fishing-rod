"""Job Hunt Tailor — FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import Base, SessionLocal, engine
from app.routers import applications, generate, health, settings
from app.seed import seed_default_settings

_settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they do not exist yet
    Base.metadata.create_all(bind=engine)
    # Seed Hamza's default profile on first run
    db = SessionLocal()
    try:
        seed_default_settings(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Job Hunt Tailor API",
    version="1.5.0",
    description="Generate tightly targeted job application materials for Hamza Salahuddin.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(generate.router)
app.include_router(applications.router)
app.include_router(settings.router)
