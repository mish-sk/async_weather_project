from difflib import get_close_matches


VALID_CITIES = {
    "Kyiv": ["Київ", "Киев"],
    "London": ["Londn"],
    "New York": ["NY", "Newyork"],
    "Tokyo": ["Токио"],
}


def normalise_city_names(city: str) -> str:
    for correct_name, alternatives in VALID_CITIES.items():
        if city in correct_name:
            return city
        elif city in alternatives:
            return correct_name

    match = get_close_matches(city, VALID_CITIES.keys(), n=1, cutoff=0.6)
    if match:
        return match[0]

    return city
