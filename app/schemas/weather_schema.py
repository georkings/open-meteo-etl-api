"""Weather schema definition for API responses."""

from typing import Dict

from pydantic import BaseModel, RootModel


class PeakValueDetail(BaseModel):
    value: float
    date_time: str


class TemperatureData(BaseModel):
    average: float
    average_by_day: Dict[str, float]
    max: PeakValueDetail
    min: PeakValueDetail
    hours_above_threshold: int
    hours_below_threshold: int


class TemperatureResponse(BaseModel):
    temperature: TemperatureData


class PrecipitationMax(BaseModel):
    value: float
    date: str


class PrecipitationData(BaseModel):
    total: float
    total_by_day: Dict[str, float]
    days_with_precipitation: int
    max: PrecipitationMax
    average: float


class PrecipitationResponse(BaseModel):
    precipitation: PrecipitationData


class PeakValueSummary(BaseModel):
    date: str
    value: float


class CitySummary(BaseModel):
    start_date: str
    end_date: str
    temperature_average: float
    precipitation_total: float
    days_with_precipitation: int
    precipitation_max: PeakValueSummary
    temperature_max: PeakValueSummary
    temperature_min: PeakValueSummary


class GeneralSummaryResponse(RootModel):
    root: Dict[str, CitySummary]
