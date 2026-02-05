"""API v1 endpoints."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.database.session import get_db
from app.schemas.weather_schema import (
    GeneralSummaryResponse,
    PrecipitationResponse,
    TemperatureResponse,
)
from app.services import stats_service
from app.utils.date_utils import validate_date_range

router = APIRouter()


@router.get("/temperature", response_model=TemperatureResponse)
def get_temperature_stats(
    city: str,
    start_date: date,
    end_date: date,
    t_high: float = settings.temp_threshold_high,
    t_low: float = settings.temp_threshold_low,
    db: Session = Depends(get_db),
):
    # Early exit if date range doesn't make sense
    validate_date_range(start_date, end_date)

    result = stats_service.get_temperature_stats(
        db, city, start_date, end_date, t_high, t_low
    )

    if isinstance(result, dict) and "error" in result:
        error_type = result["error"]
        if error_type == "CITY_NOT_FOUND":
            raise HTTPException(
                status_code=404, detail=f"City '{city}' not found in our database."
            )
        if error_type == "OUT_OF_RANGE":
            raise HTTPException(
                status_code=400,
                detail=f"Dates out of range. Data available from {result['db_min']} to {result['db_max']}",
            )
        raise HTTPException(status_code=404, detail="No data available for this city")

    return result


@router.get("/precipitation", response_model=PrecipitationResponse)
def get_precipitation_stats(
    city: str, start_date: date, end_date: date, db: Session = Depends(get_db)
):
    # Early exit if date range doesn't make sense
    validate_date_range(start_date, end_date)

    result = stats_service.get_precipitation_stats(db, city, start_date, end_date)

    if isinstance(result, dict) and "error" in result:
        error_type = result["error"]
        if error_type == "CITY_NOT_FOUND":
            raise HTTPException(
                status_code=404, detail=f"City '{city}' not found in our database."
            )
        if error_type == "OUT_OF_RANGE":
            raise HTTPException(
                status_code=400,
                detail=f"Dates out of range. Data available from {result['db_min']} to {result['db_max']}",
            )
        raise HTTPException(status_code=404, detail="No data available for this city")

    return result


@router.get("/general", response_model=GeneralSummaryResponse)
def get_general_stats(db: Session = Depends(get_db)):
    """
    Returns a global summary of all cities in the database.
    Calculates averages and totals per city.
    """
    return stats_service.get_all_cities_summary(db)
