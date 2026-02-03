# open-meteo-etl-api

**open-meteo-etl-api** is a robust data engineering solution designed to fetch, store, and analyze historical weather data. It bridges the gap between raw external data and actionable insights through a clean ETL pipeline and a FastAPI-powered REST interface.

The project demonstrates a professional Python architecture, leveraging Pandas for high-performance data manipulation and SQLAlchemy for reliable persistence.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **Data Analysis**: Pandas
- **Database (ORM)**: SQLAlchemy (SQLite)
- **External APIs**: Open-Meteo (Geocoding & Archive)
- **CLI Tooling**: Argparse

## 🏗️ Project Structure

```
open-meteo-etl-api/
├── app/
│   ├── api/          # REST endpoints
│   ├── database/     # DB connection and session management
│   ├── models/       # SQLAlchemy database models
│   ├── schemas/      # Pydantic validation schemas
│   └── services/     # Business logic & Pandas processing
├── scripts/          # CLI scripts for data loading (ETL)
├── data/             # Local storage for SQLite DB
├── tests/            # Unit tests
└── README.md
```

## 🚀 Getting Started

**1. Installation**

**2. Loading Data (ETL)**

**3. Running the API**

## 🧪 Testing
The project uses `pytest` with `httpx` for integration testing and service mocking.

Run all tests:
```bash
python -m pytest
```
## 🐳 Docker Deployment

## 📊 API Endpoints

## 💡 Key Technical Decisions

## ✅ What Could Be Added Next
