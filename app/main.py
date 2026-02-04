"""Main entry point for the application."""

from fastapi import FastAPI

from app.api.base import router as api_router
from app.core.settings import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API de Clima. Ve a /docs para ver la documentación."
    }
