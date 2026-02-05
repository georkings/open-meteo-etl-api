"""Tests for the API endpoints."""

from datetime import date

from app.models.city import City
from app.models.weather import WeatherData

# --- HELPER TO POPULATE TEST DATA ---


def seed_test_data(db_session):
    """Utility to seed the test database with predictable data."""
    madrid = City(id=1, name="Madrid", latitude=40.4, longitude=-3.7)
    db_session.add(madrid)

    # Add two days of data
    day1 = date(2026, 1, 1)
    day2 = date(2026, 1, 2)

    records = [
        # Day 1: 1.5mm rain, 20 degrees
        WeatherData(city_id=1, temperature=20.0, precipitation=1.5, timestamp=day1),
        # Day 2: 0.5mm rain, 30 degrees
        WeatherData(city_id=1, temperature=30.0, precipitation=0.5, timestamp=day2),
    ]
    db_session.add_all(records)
    db_session.commit()
    return madrid


# --- TEMPERATURE ENDPOINT TESTS ---


def test_get_temperature_stats_success(client, db_session):
    seed_test_data(db_session)

    response = client.get(
        "/api/v1/temperature",
        params={
            "city": "Madrid",
            "start_date": "2026-01-01",
            "end_date": "2026-01-02",
            "t_above": 25.0,
            "t_below": 10.0,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["temperature"]["average"] == 25.0
    assert "2026-01-01" in data["temperature"]["average_by_day"]


def test_temperature_city_not_found(client, db_session):
    # No data seeded
    response = client.get(
        "/api/v1/temperature",
        params={
            "city": "Atlantis",
            "start_date": "2026-01-01",
            "end_date": "2026-01-02",
        },
    )

    assert response.status_code == 404
    assert "not found in our database" in response.json()["detail"]


# --- PRECIPITATION ENDPOINT TESTS ---


def test_get_precipitation_stats_success(client, db_session):
    seed_test_data(db_session)

    response = client.get(
        "/api/v1/precipitation",
        params={"city": "Madrid", "start_date": "2026-01-01", "end_date": "2026-01-02"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["precipitation"]["total"] == 2.0
    assert data["precipitation"]["days_with_precipitation"] == 2
    assert data["precipitation"]["max"]["value"] == 1.5  # Max is day 1


def test_precipitation_out_of_range(client, db_session):
    seed_test_data(db_session)

    # Requesting dates from 2025 when we only have 2026
    response = client.get(
        "/api/v1/precipitation",
        params={"city": "Madrid", "start_date": "2025-01-01", "end_date": "2025-01-02"},
    )

    assert response.status_code == 400
    assert "Dates out of range" in response.json()["detail"]


# --- GENERAL SUMMARY TESTS ---


def test_get_general_summary_success(client, db_session):
    seed_test_data(db_session)

    response = client.get("/api/v1/general")

    assert response.status_code == 200
    data = response.json()

    assert "Madrid" in data
    assert data["Madrid"]["temperature_average"] == 25.0
    assert data["Madrid"]["precipitation_total"] == 2.0


def test_general_summary_empty(client, db_session):
    # No data seeded
    response = client.get("/api/v1/general")

    assert response.status_code == 200
    assert response.json() == {}
