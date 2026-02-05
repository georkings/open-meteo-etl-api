"""Stats service for temperature and precipitation calculations."""

from datetime import date, timedelta

import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.city import City
from app.models.weather import WeatherData


def _get_weather_data(db: Session, city_name: str, start_date: date, end_date: date):
    """Internal helper to validate city, check range, and return a DataFrame."""
    # 1. City existence
    city = db.query(City).filter(City.name.ilike(city_name)).first()
    if not city:
        return None, {"error": "CITY_NOT_FOUND"}

    # 2. Coverage Check (Min/Max in DB)
    range_query = (
        db.query(func.min(WeatherData.timestamp), func.max(WeatherData.timestamp))
        .filter(WeatherData.city_id == city.id)
        .first()
    )

    db_min, db_max = range_query
    if not db_min or not db_max:
        return None, {"error": "NO_DATA_AVAILABLE"}

    if start_date < db_min.date() or end_date > db_max.date():
        return None, {
            "error": "OUT_OF_RANGE",
            "db_min": str(db_min.date()),
            "db_max": str(db_max.date()),
        }

    # 3. Load Data
    query = (
        db.query(WeatherData)
        .join(City)
        .filter(
            City.name.ilike(city_name),
            WeatherData.timestamp >= start_date,
            WeatherData.timestamp <= end_date + timedelta(days=1),
        )
    )
    df = pd.read_sql(query.statement, db.get_bind())

    if df.empty:
        return None, {"error": "NO_DATA_AVAILABLE"}

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df, None


def get_temperature_stats(
    db: Session,
    city_name: str,
    start_date: date,
    end_date: date,
    t_above: float,
    t_below: float,
):
    df, error = _get_weather_data(db, city_name, start_date, end_date)
    if error:
        return error

    # Calculate average temperature by day
    avg_by_day = df.groupby(df["timestamp"].dt.date)["temperature"].mean()
    avg_by_day_dict = {str(date): round(temp, 1) for date, temp in avg_by_day.items()}

    # idxmax returns the index (timestamp) of the peak values
    max_idx = df["temperature"].idxmax()
    min_idx = df["temperature"].idxmin()

    # Returning keys that match response schema
    return {
        "temperature": {
            "average": round(df["temperature"].mean(), 1),
            "average_by_day": avg_by_day_dict,
            "max": {
                "value": df.loc[max_idx, "temperature"],
                "date_time": df.loc[max_idx, "timestamp"].strftime("%Y-%m-%dT%H:%M"),
            },
            "min": {
                "value": df.loc[min_idx, "temperature"],
                "date_time": df.loc[min_idx, "timestamp"].strftime("%Y-%m-%dT%H:%M"),
            },
            "hours_above_threshold": (df["temperature"] > t_above).sum(),
            "hours_below_threshold": (df["temperature"] < t_below).sum(),
        }
    }


def get_precipitation_stats(
    db: Session, city_name: str, start_date: date, end_date: date
):
    df, error = _get_weather_data(db, city_name, start_date, end_date)
    if error:
        return error

    # Group by day to get daily totals
    daily_totals = df.groupby(df["timestamp"].dt.date)["precipitation"].sum()

    # Identify the day with the absolute maximum precipitation
    max_day = daily_totals.idxmax()
    max_value = daily_totals.max()

    return {
        "precipitation": {
            "total": round(df["precipitation"].sum(), 2),
            "total_by_day": {str(k): round(v, 1) for k, v in daily_totals.items()},
            "days_with_precipitation": (daily_totals > 0).sum(),
            "max": {"value": round(max_value, 2), "date": str(max_day)},
            "average": round(daily_totals.mean(), 2),
        }
    }


def get_all_cities_summary(db: Session):
    # 1. Fetch raw data with City names
    query = (
        db.query(
            City.name,
            WeatherData.timestamp,
            WeatherData.temperature,
            WeatherData.precipitation,
        )
        .join(WeatherData)
        .statement
    )

    df = pd.read_sql(query, db.get_bind())

    if df.empty:
        return {}

    # Convert timestamp to date for the "max/min date" requirement
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date

    result = {}

    # 2. Group by city name and iterate
    for city_name, group in df.groupby("name"):
        # Find rows with max/min values to get their dates
        max_temp_row = group.loc[group["temperature"].idxmax()]
        min_temp_row = group.loc[group["temperature"].idxmin()]
        max_precip_row = group.loc[group["precipitation"].idxmax()]

        # Count days with precipitation (assuming > 0 is a rainy day)
        # We group by date first so we don't count multiple rainy hours in one day twice
        daily_precip = group.groupby("date")["precipitation"].sum()
        days_with_precip = (daily_precip > 0).sum()

        result[city_name] = {
            "start_date": str(group["date"].min()),
            "end_date": str(group["date"].max()),
            "temperature_average": round(group["temperature"].mean(), 1),
            "precipitation_total": round(group["precipitation"].sum(), 1),
            "days_with_precipitation": days_with_precip,
            "precipitation_max": {
                "date": str(max_precip_row["date"]),
                "value": max_precip_row["precipitation"],
            },
            "temperature_max": {
                "date": str(max_temp_row["date"]),
                "value": max_temp_row["temperature"],
            },
            "temperature_min": {
                "date": str(min_temp_row["date"]),
                "value": min_temp_row["temperature"],
            },
        }

    return result
