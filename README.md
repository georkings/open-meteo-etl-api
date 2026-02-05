# ☁️ Open-Meteo ETL & Analytics API

A robust FastAPI application that extracts weather data from the Open-Meteo API, transforms it using Pandas, and stores it in a SQLite/PostgreSQL database. The project includes endpoints to calculate temperature and precipitation statistics.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **Data Analysis**: Pandas
- **Database (ORM)**: SQLAlchemy (SQLite)
- **External APIs**: Open-Meteo (Geocoding & Archive)
- **CLI Tooling**: Argparse

## 🚀 Features

- **ETL Pipeline:** Clean and reload synchronization strategy to ensure data consistency.

- **Pandas Integration:** High-performance weather calculations (averages, thresholds, daily totals).

- **FastAPI Backend:** Fully typed responses using Pydantic schemas.

- **Logging & Error Handling:** Comprehensive logging for database sessions and service logic.

- **Testing Suite:** Robust unit and integration tests using pytest and in-memory SQLite.

- **Dockerized:** Ready for containerized deployment.

## 🏗️ Project Structure

```
open-meteo-etl-api/
├── app/
│   ├── api/            # REST endpoints
│   ├── core/           # Configuration and settings
│   ├── database/       # Session management
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic validation schemas
│   ├── services/       # Business logic (Stats & Sync)
│   └── main.py         # FastAPI entry point
├── data/               # Local storage for SQLite DB
├── scripts/
│   └── load_data.py    # CLI script to trigger ETL sync
├── tests/              # Pytest suite
├── Dockerfile          # Container definition
└── requirements.txt    # Python dependencies
```

## ⚙️ Installation & Setup

**1. Clone and Environment**
```bash
git clone https://github.com/georkings/open-meteo-etl-api.git
cd open-meteo-etl-api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Loading Data (ETL)**

Before starting the API, populate your database with weather data with the following format:
```bash
python -m scripts.load_data Havana 2024-01-01 2024-01-05
```

## 🏃 Running the Application

**Local Development**
```bash
uvicorn app.main:app --reload
```
Access the interactive API documentation (Swagger UI) at: http://localhost:8000/docs

**Using Docker**
```bash
docker build -t weather-api .
docker run -p 8000:8000 weather-api
```

## 🧪 Testing

The project uses `pytest` with a dedicated in-memory database to ensure tests are fast and isolated.

```bash
# Run all tests
python -m pytest

# Run with coverage report
python -m pytest --cov=app
```

## 📊 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Liveness probe / Health check |
| `GET` | `/api/v1/temperature` | Temperature stats for a city |
| `GET` | `/api/v1/precipitation` | Precipitation stats for a city |
| `GET` | `/api/v1/general` | Summary of all cities currently in the database. |
