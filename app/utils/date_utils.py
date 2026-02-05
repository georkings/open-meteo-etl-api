"""Utility functions for date validation and manipulation."""

from datetime import date

from fastapi import HTTPException


def validate_date_range(start: date, end: date):
    """Checks if start date is before or equal to end date."""
    if start > end:
        raise HTTPException(
            status_code=400,
            detail=f"Start date ({start}) cannot be after end date ({end}).",
        )
    return True
