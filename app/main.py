"""Main entry point for the application."""

import logging

from fastapi import FastAPI

from app.api.base import router as api_router
from app.api.system import router as system_router
from app.core.logging import setup_logging
from app.core.settings import settings
from app.database.session import engine
from app.models.base import Base

# Create the tables on startup (only if they don't exist)
Base.metadata.create_all(bind=engine)

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

logger.info("Creating FastAPI application")
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(api_router, prefix="/api")
logger.debug("API router mounted at /api")

app.include_router(system_router)
logger.debug("System router mounted")


@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API de Clima. Ve a /docs para ver la documentación."
    }
