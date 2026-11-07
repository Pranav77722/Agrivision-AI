import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Query
from app.services.weather_service import WeatherService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/weather", tags=["Agro-Meteorology"])


@router.get(
    "/current",
    response_model=Dict[str, Any],
    summary="Get real live weather and spraying advisory",
    description="Fetch real live temperature, humidity, wind conditions, and automated pesticide spraying recommendations from Open-Meteo."
)
async def get_current_weather(
    district: Optional[str] = Query("Pune", description="District or city name in India"),
    state: Optional[str] = Query("Maharashtra", description="State name"),
    lat: Optional[float] = Query(None, description="GPS Latitude"),
    lon: Optional[float] = Query(None, description="GPS Longitude")
) -> Dict[str, Any]:
    service = WeatherService()
    return await service.get_current_weather(district=district, state=state, lat=lat, lon=lon)


@router.get(
    "/forecast",
    response_model=List[Dict[str, Any]],
    summary="Get multi-day agricultural weather forecast",
    description="Retrieve 5-day weather forecast with rain probability and crop spraying advisories from Open-Meteo."
)
async def get_forecast(
    district: Optional[str] = Query("Pune", description="District name"),
    days: int = Query(5, ge=1, le=7, description="Number of days"),
    lat: Optional[float] = Query(None, description="GPS Latitude"),
    lon: Optional[float] = Query(None, description="GPS Longitude")
) -> List[Dict[str, Any]]:
    service = WeatherService()
    return await service.get_forecast(district=district, days=days, lat=lat, lon=lon)
