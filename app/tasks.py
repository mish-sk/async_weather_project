from app.celery_app import celery
from app.services.weather_service import weather_fetch


@celery.task
def fetch_weather_task(city: str):
    return weather_fetch(city)
