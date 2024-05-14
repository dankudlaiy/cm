areas = {
    "United States": "00",
    "Alabama": "01",
    "Alaska": "02",
    "Arizona": "04",
    "Arkansas": "05",
    "California": "06",
    "Colorado": "08",
    "Connecticut": "09",
    "Delaware": "10",
    "Florida": "12",
    "Georgia": "13",
    "Hawaii": "15",
    "Kentucky": "21",
    "Michigan": "26",
    "Mississippi": "28",
    "Nebraska": "31",
    "New Jersey": "34",
    "New Mexico": "35",
    "New York": "36",
    "Ohio": "39",
    "Texas": "48"
}


def to_area_code(country):
    return areas.get(country)


def to_country_name(code):
    return next((k for k, v in areas.items() if v == code), None)
