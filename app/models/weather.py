"""WeatherData model definition."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

# This prevents the "City is not defined" error during type checking
if TYPE_CHECKING:
    from app.models.city import City


class WeatherData(Base):
    """
    Stores hourly weather measurements.
    Uses SQLAlchemy 2.0 Mapped/mapped_column syntax.
    """

    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign Key linking to the City table
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"), nullable=False
    )

    # Measurements
    timestamp: Mapped[datetime] = mapped_column(nullable=False, index=True)
    temperature: Mapped[float] = mapped_column(nullable=False)
    precipitation: Mapped[float] = mapped_column(nullable=False)

    # Relationship back to the City model
    city: Mapped["City"] = relationship("City", back_populates="weather_records")

    def __repr__(self) -> str:
        return f"<WeatherData(city_id={self.city_id}, time='{self.timestamp}', temp={self.temperature})>"
