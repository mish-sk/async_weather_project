import logging
import re

VALID_CITIES = {
    "Kyiv": ["Київ", "Киев"],
    "London": ["Londn"],
    "New York": ["NY", "Newyork"],
    "Tokyo": ["Токио"],
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def validate_city_name(city: str) -> bool:
    return bool(re.match(r"^[A-Za-zА-Яа-яЁёҐґІіЇїЄє\s\-]+$", city))


def normalise_city_names(city: str) -> str:
    city = city.strip().title()
    for normalized, variations in VALID_CITIES.items():
        if city in variations or city == normalized:
            return normalized
    return city


def process_cities(cities: list[str]) -> list[str]:
    valid_cities = []
    for city in cities:
        if validate_city_name(city):
            normalized_city = normalise_city_names(city)
            logging.info(f"Normalized city: {city} -> {normalized_city}")
            valid_cities.append(normalized_city)
        else:
            logging.warning(f"Invalid city name: {city}")

    return valid_cities
