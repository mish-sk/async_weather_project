from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.utils import normalise_city_names


app = FastAPI()


class CityRequest(BaseModel):
    cities: List[str]


@app.post("/weather")
async def get_weather(request: CityRequest):
    if not request:
        raise HTTPException(status_code=400, detail="City list cannot be empty")

    normalised_cities = []

    for city in request.cities:
        normalised_cities.append(normalise_city_names(city))

    return {"message": "Request received", "normalised_cities": normalised_cities}

