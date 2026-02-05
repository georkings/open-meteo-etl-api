"""Script to load weather data into the local database."""

import argparse
import logging

import requests

from app.core.logging import setup_logging
from app.core.settings import settings
from app.database.session import SessionLocal, engine
from app.models import Base, City, WeatherData  # noqa: F401
from app.services.weather_service import store_weather_in_db

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


def load_weather_data(city_name: str, start_date: str, end_date: str):
    # Ensure the database and tables exist before doing anything else
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # 1. Fetch Coordinates (Geocoding)
        logger.info(f"🔍 Searching coordinates for {city_name}...")
        geo_params = {"name": city_name, "count": 1, "language": "en"}
        geo_res = requests.get(settings.geo_url, params=geo_params).json()

        if not geo_res.get("results"):
            logger.warning(f"❌ Error: City '{city_name}' not found.")
            return

        location = geo_res["results"][0]
        lat, lon = location["latitude"], location["longitude"]

        # 2. Ensure City exists in DB
        db_city = db.query(City).filter(City.name == city_name).first()
        if not db_city:
            db_city = City(name=city_name, latitude=lat, longitude=lon)
            db.add(db_city)
            db.commit()
            db.refresh(db_city)
            logger.info(f"✅ Created new city entry for {city_name}.")
        else:
            logger.warning(
                f"⚠️ City {city_name} already exists. Old data will be overwritten."
            )

        # 3. Fetch Weather Data (Archive)
        logger.info(f"⏳ Downloading weather from {start_date} to {end_date}...")
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "temperature_2m,precipitation",
        }
        weather_res = requests.get(settings.archive_url, params=weather_params).json()

        # 4. Save to DB using the Service
        store_weather_in_db(db, db_city.id, weather_res)
        logger.info(f"🚀 Success! Data for {city_name} is now synchronized.")

    except Exception as e:
        logger.error(f"💥 An error occurred: {e}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Extract weather data from Open-Meteo and load it into the local database."
    )

    # Required arguments
    parser.add_argument("city", type=str, help="Name of the city (e.g., Madrid)")
    parser.add_argument("start", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("end", type=str, help="End date in YYYY-MM-DD format")

    args = parser.parse_args()

    # Basic validation for dates could be added here
    load_weather_data(args.city, args.start, args.end)


if __name__ == "__main__":
    main()
