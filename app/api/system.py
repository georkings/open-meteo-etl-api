"""System endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db

router = APIRouter()


@router.get("/health", tags=["Monitoring"])
def health_check(db: Session = Depends(get_db)):
    """
    Verify the API and Database connection are functional.
    """
    try:
        # Execute a simple query to test the DB connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        # Log the error here in a real app
        raise HTTPException(
            status_code=503, detail=f"Database connection failed: {str(e)}"
        )
