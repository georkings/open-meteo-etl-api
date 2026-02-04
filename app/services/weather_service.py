"""Service to handle weather data storage and synchronization."""

import pandas as pd
from sqlalchemy.orm import Session

from app.models.weather import WeatherData


def store_weather_in_db(db: Session, city_id: int, api_response: dict):
    """
    Processes the Open-Meteo API response and synchronizes the database.
    Implements a 'Clean and Reload' strategy for the specific city.
    """

    # 1. Prepare new data using Pandas
    # Extracting the hourly data dictionary from the API response
    hourly_data = api_response.get("hourly", {})

    if not hourly_data:
        print(f"⚠️ No hourly data found in API response for city_id {city_id}")
        return

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(hourly_data["time"]),
            "temperature": hourly_data["temperature_2m"],
            "precipitation": hourly_data["precipitation"],
            "city_id": city_id,
        }
    )

    try:
        # 2. TOTAL CLEANUP: Delete ALL previous records for this city.
        # This ensures the stored date range is consistent and contains no gaps
        # or overlapping duplicates from previous partial loads.
        db.query(WeatherData).filter(WeatherData.city_id == city_id).delete()

        # COMMIT the delete immediately to release the write lock
        db.commit()

        # 3. Bulk Insertion
        # We use db.get_bind() to use the current session's connection.
        # 'if_exists="append"' is used because we just cleared the specific rows,
        # but we want to keep the table structure intact.
        df.to_sql(
            "weather_data",
            con=db.get_bind(),
            if_exists="append",
            index=False,  # Do not write DataFrame index as a column
            method="multi",  # Improves performance for batch inserts
        )

        # 4. Finalize the transaction
        db.commit()
        print(f"✅ Successfully synchronized {len(df)} records for city_id {city_id}")

    except Exception as e:
        db.rollback()
        print(f"❌ Failed to store weather data: {e}")
        raise e
