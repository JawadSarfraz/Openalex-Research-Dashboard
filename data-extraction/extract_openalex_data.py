# data-extraction/extract_openalex_data.py

import os
import requests
import json
from config import OPENALEX_API_KEY

BASE_URL = "https://api.openalex.org/works"
HEADERS = {
    "Authorization": f"Bearer {OPENALEX_API_KEY}"
}

def fetch_data(field, country, start_year, end_year):
    url = (
        f"{BASE_URL}?filter=from_publication_date:{start_year}-01-01,"
        f"to_publication_date:{end_year}-12-31,"
        f"concepts.id:{field},"
        f"author.country_code:{country}"
    )

    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        save_data(data, country, field, start_year, end_year)
    else:
        print(f"Error fetching data: {response.status_code}")

def save_data(data, country, field, start_year, end_year):
    filename = f"raw_data/{country}_{field}_{start_year}_{end_year}.json"
    os.makedirs("raw_data", exist_ok=True)

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Example usage
    fetch_data("C123456", "US", 2010, 2020)
