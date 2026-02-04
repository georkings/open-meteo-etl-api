"""Application settings and environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Open-Meteo Weather API"
    app_description: str = (
        "API para consultar estadísticas históricas de clima cargadas en DB local."
    )
    app_version: str = "1.0.0"


settings = Settings()
