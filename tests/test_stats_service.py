"""Unit tests for stats_service.py."""

from datetime import date

from app.models.city import City
from app.models.weather import WeatherData
from app.services import stats_service


def test_get_temperature_stats_city_not_found(db_session):
    # Setup: Ensure the DB is empty (no cities added)

    # Execute
    from datetime import date

    result = stats_service.get_temperature_stats(
        db_session, "Atlantis", date(2026, 1, 1), date(2026, 1, 2), 30.0, 0.0
    )

    # Assert: Check for our custom error code
    assert result == {"error": "CITY_NOT_FOUND"}


def test_get_temperature_stats_no_data(db_session):
    # Setup: Add a city but no weather data
    city = City(id=1, name="Madrid", latitude=40.4, longitude=-3.7)
    db_session.add(city)
    db_session.commit()

    # Execute
    result = stats_service.get_temperature_stats(
        db_session, "Madrid", date(2024, 7, 1), date(2024, 7, 2), 30.0, 0.0
    )

    # Assert: Check for our custom error code
    assert result == {"error": "NO_DATA_AVAILABLE"}


def test_get_temperature_stats_out_of_range(db_session):
    # Setup: Add a city and some weather data with a limited date range
    city = City(id=1, name="Madrid", latitude=40.4, longitude=-3.7)
    db_session.add(city)
    db_session.add(
        WeatherData(
            city_id=1, temperature=20.0, precipitation=0.0, timestamp=date(2024, 7, 1)
        )
    )
    db_session.commit()

    # Execute: Request a date range that is outside the DB coverage
    result = stats_service.get_temperature_stats(
        db_session, "Madrid", date(2024, 6, 1), date(2024, 6, 30), 30.0, 0.0
    )

    # Assert: Check for our custom error code and DB coverage info
    assert result == {
        "error": "OUT_OF_RANGE",
        "db_min": "2024-07-01",
        "db_max": "2024-07-01",
    }


def test_get_temperature_stats_success(db_session):
    # 1. Setup: Add a city and some dummy weather data
    city = City(id=1, name="Madrid", latitude=40.4, longitude=-3.7)
    db_session.add(city)
    db_session.commit()

    test_data = [
        WeatherData(
            city_id=1, temperature=20.0, precipitation=0.0, timestamp=date(2024, 7, 1)
        ),
        WeatherData(
            city_id=1, temperature=30.0, precipitation=1.0, timestamp=date(2024, 7, 2)
        ),
    ]
    db_session.add_all(test_data)
    db_session.commit()

    # 2. Execute
    result = stats_service.get_temperature_stats(
        db_session, "Madrid", date(2024, 7, 1), date(2024, 7, 2), 25.0, 10.0
    )

    # 3. Assert
    assert "temperature" in result
    assert result["temperature"]["average"] == 25.0
    assert result["temperature"]["max"]["value"] == 30.0
    assert result["temperature"]["hours_above_threshold"] == 1
