# Asynchronous Weather API Project

An asynchronous weather API Project using FastAPI, Celery, and Redis.

## Features
- Fetch weather data asynchronously
- Store results by region
- Track task progress using task IDs
- Retrieve stored weather data

## Installation

Make sure you have Python installed. Clone the repository and set up the environment:

```
git clone https://github.com/mish-sk/async_weather_project
cd async_weather_project
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

Create a `.env` file and add your API key:
```
WEATHER_API_KEY=<your_weatherapi_key>
```

## Running the Application

Start Redis Docker:
```
docker run -d --name redis -p 6379:6379 redis
```

Start the Celery worker:
```
celery -A app.celery_app worker --loglevel=info
```

Run the FastAPI server:
```
uvicorn app.main:app --reload
```

## API Usage

### Request Weather Data
```
POST /weather
```
Example:
```
curl -X POST "http://127.0.0.1:8000/weather" -H "Content-Type: application/json" -d '{"cities": ["Kyiv", "New York"]}'
```

### Check Task Status
```
GET /tasks/{task_id}
```
Example:
```
curl -X GET "http://127.0.0.1:8000/tasks/task-id"
```

### Retrieve Stored Results
```
GET /results/{region}
```
Example:
```
curl -X GET "http://127.0.0.1:8000/results/New_York"
```

## License

This project is licensed under the MIT License.
