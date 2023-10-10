import json

import requests
from requests.structures import CaseInsensitiveDict

from utils.settings import APIKEY_JSON


def get_encouragement_quote():
    response = requests.get("https://zenquotes.io/api/quotes/")
    json_data = json.loads(response.text)
    discord_response = f"""I have {len(json_data)}
different encouragement quotations for you.
A quote by {json_data[0]['a']} has been radomly chosen:
\"{json_data[0]['q']}\""""

    return discord_response


# TODO: validations to city and country
def get_city_temperature(country, city):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    response = requests.get(
        f"https://api.geoapify.com/v1/geocode/search?apiKey={APIKEY_JSON}&city={city}&country={country}",
        headers=headers,
    )
    response_json_data = json.loads(response.text)

    longitude = response_json_data["features"][0]["properties"]["lon"]
    latitude = response_json_data["features"][0]["properties"]["lat"]

    # get temperature according to long and lat
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?longitude={longitude}&latitude={latitude}&current_weather=true"
    )
    response_json_data = json.loads(response.text)
    temperature = response_json_data["current_weather"]["temperature"]

    description = f"Today in {city}, {country}, the temperature is {temperature}°C"

    return description


def get_all_products(name=None, category=None, limit=None):
    if limit:
        headers = CaseInsensitiveDict()
        response = requests.get(
            f"https://fakestoreapi.com/products?limit={limit}", headers=headers
        )

        # get all products to the list
        json_response = json.loads(response.text)
        display_all_products = ""

        for index, item in list(enumerate(json_response)):
            display_all_products += f"{index}. {item['title']}, ${item['price']}\n"

        return display_all_products
