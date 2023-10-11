import json

import requests
from requests.structures import CaseInsensitiveDict

from utils.settings import APIKEY_GEO, APIKEY_JSON

from .validators import ValidationView as validation


def get_encouragement_quote():
    response = requests.get("https://zenquotes.io/api/quotes/")
    json_data = json.loads(response.text)
    discord_response = f"""I have {len(json_data)}
different encouragement quotations for you.
A quote by {json_data[0]['a']} has been radomly chosen:
\"{json_data[0]['q']}\""""

    return discord_response


def get_city_temperature(country, city):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    country_exist = check_country_validity(country, headers)

    if country_exist:
        response = requests.get(
            f"https://api.geoapify.com/v1/geocode/search?apiKey={APIKEY_JSON}&city={city}&country={country}",
            headers=headers,
        )
        response_json_data = json.loads(response.text)

        longitude = response_json_data["features"][0]["properties"]["lon"]
        latitude = response_json_data["features"][0]["properties"]["lat"]

        # get temperature according to long and lat
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast?longitude={longitude}&latitude={latitude}&current_weather=true",
            headers=headers,
        )
        response_json_data = json.loads(response.text)
        temperature = response_json_data["current_weather"]["temperature"]

        description = f"Today in {city}, {country}, the temperature is {temperature}°C"

        return description
    else:
        return validation.no_country_validation()


def check_country_validity(country, headers):
    response = requests.get(
        f"https://api.opencagedata.com/geocode/v1/json?q={country}&key={APIKEY_GEO}"
    )

    response_json_data = json.loads(response.text)

    # check if country exists
    if response_json_data["total_results"] == 0:
        return False
    else:
        return True


def get_store_products(name: str = None, category: str = None, limit: str = None):
    headers = CaseInsensitiveDict()
    display_all_products = ""

    if limit:
        response = requests.get(
            f"https://fakestoreapi.com/products?limit={limit}", headers=headers
        )

        # get all products to the list
        json_response = json.loads(response.text)

        for index, product in list(enumerate(json_response)):
            display_all_products += (
                f"{index}. {product['title']}, ${product['price']}\n"
            )
    elif category:
        category = category.lower().strip()
        response = requests.get(
            f"https://fakestoreapi.com/products/category/{category}", headers=headers
        )

        json_response = json.loads(response.text)

        if len(json_response) == 0:
            return validation.no_category_valdation()

        for index, product in list(enumerate(json_response)):
            display_all_products += (
                f"{index}. {product['title']}, ${product['price']}\n"
            )
    elif name:
        name = name.lower().strip()
        response = requests.get("https://fakestoreapi.com/products/", headers=headers)

        json_response = json.loads(response.text)
        get_products_by_name = [
            product
            for product in json_response
            if name in product["title"].lower().split()
        ]

        if len(get_products_by_name) == 0:
            return validation.no_product_valdation()

        for index, product in list(enumerate(get_products_by_name)):
            display_all_products += (
                f"{index}. {product['title']}, ${product['price']}\n"
            )
    else:
        # if nothing has been provided, return all categories
        response = requests.get(
            "https://fakestoreapi.com/products/categories", headers=headers
        )

        json_response = json.loads(response.text)
        print(json_response)

        for index, category in list(enumerate(json_response)):
            display_all_products += f"{index}. {category}\n"

    return display_all_products
