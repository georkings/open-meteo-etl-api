"""City model definition."""

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

# This prevents the "City is not defined" error during type checking
if TYPE_CHECKING:
    from app.models.weather import WeatherData


class City(Base):
    """
    Represents a city in the system.
    Using SQLAlchemy 2.0 modern syntax with string-based forward references.
    """

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    # We use "WeatherData" as a string to avoid importing it here.
    # This prevents circular dependency issues.
    weather_records: Mapped[list["WeatherData"]] = relationship(
        "WeatherData", back_populates="city", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<City(name='{self.name}', lat={self.latitude}, lon={self.longitude})>"
