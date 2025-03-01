import httpx
import os

from dotenv import load_dotenv


load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is missing.")


async def weather_fetch(city: str):

    base_url = "http://api.weatherapi.com/v1/current.json"

    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "aqi": "no"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            return {
                "city": city,
                "temperature": data["current"]["temp_c"],
                "description": data["current"]["condition"]["text"]
            }

        except httpx.HTTPStatusError as e:
            print(f"Error: {e}")
            return {"error": f"API error for {city} {e.response.status_code}"}

        except Exception as e:
            print(f"Error: {e}")
            return {"error": f"Unexpected error for {city} {str(e)}"}
