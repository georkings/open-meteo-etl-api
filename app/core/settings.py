"""Application settings and environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Open-Meteo Weather API"
    app_description: str = (
        "API para consultar estadísticas históricas de clima cargadas en DB local."
    )
    app_version: str = "1.0.0"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./data/sql_app.db"
    testing_database_url: str = "sqlite:///:memory:"
    geo_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    archive_url: str = "https://archive-api.open-meteo.com/v1/archive"
    temp_threshold_high: float = 30.0
    temp_threshold_low: float = 0.0


settings = Settings()
