from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()


class CityRequest(BaseModel):
    cities: List[str]


@app.post("/weather")
async def get_weather(request: CityRequest):
    if not request:
        raise HTTPException(status_code=400, detail="City list cannot be empty")
    return {"message": "Request received", "cities": request.cities}
