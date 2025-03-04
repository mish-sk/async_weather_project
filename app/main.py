import json
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.utils import process_cities
from app.services.weather_service import weather_fetch
from app.tasks import fetch_weather_task


RESULTS_DIR = "weather_data"
app = FastAPI()


class CityRequest(BaseModel):
    cities: List[str]


@app.post("/weather")
def get_weather(request: CityRequest):
    if not request:
        raise HTTPException(status_code=400, detail="City list cannot be empty")

    normalised_cities = process_cities(request.cities)

    weather_data = [weather_fetch(city) for city in normalised_cities]

    tasks_id = [fetch_weather_task.delay(city).id for city in normalised_cities]

    return {"message": "Request received", "data": weather_data, "tasks_id": tasks_id}


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = fetch_weather_task.AsyncResult(task_id)
    return {"task_id": task_id, "status": task.status, "result": task.result}


@app.get("/results/{region}")
def get_results(region: str):
    region_path = os.path.join(RESULTS_DIR, region.lower())

    if not os.path.exists(region_path):
        raise HTTPException(status_code=404, detail=f"Region {region} not found")

    results = []
    for file_name in os.listdir(region_path):
        file_path = os.path.join(region_path, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            results.append(json.load(f))

    return {"region": region, "data": results}
