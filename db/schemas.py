from pydantic import BaseModel

from .models import datetime


class CitiesScheme(BaseModel):
    """Модель для преобразования из орм модели в Pydantic схему"""
    city: str
    weather_info_today: str | None

    weather_forecast_for_1_day: str | None
    weather_forecast_for_2_day: str | None
    weather_forecast_for_3_day: str | None

    air_quality_today: str | None

    today_update_on: datetime
    days_3_update_on: datetime
    air_quality_update_on: datetime

    class Config:
        """Конфигурация модели Pydantic"""
        from_attributes = True  # для орм грубо говоря