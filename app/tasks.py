import json
import os
import logging

from app.celery_app import celery
from app.services.weather_service import weather_fetch

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

RESULT_DIR = "weather_data"


@celery.task
def fetch_weather_task(city: str):
    try:
        data = weather_fetch(city)
        if not data:
            logging.warning(f"Failed to fetch data for {city}")
            return None

        region = data.get("region", "unknown").lower()
        task_id = fetch_weather_task.request.id

        region_path = os.path.join(RESULT_DIR, region)
        os.makedirs(region_path, exist_ok=True)
        file_path = os.path.join(region_path, f"task_{task_id}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Weather data for {city} saved {file_path}")
        return file_path

    except Exception as e:
        logging.error(f"Error processing {city}: {e}")
        return None
