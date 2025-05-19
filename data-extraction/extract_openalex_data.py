import os
import requests
import json  # <-- Add this line
from dotenv import load_dotenv

load_dotenv()

RAW_DATA_PATH = "data-extraction/raw_data/"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

OPENALEX_API_KEY = os.getenv("OPENALEX_API_KEY")

def fetch_openalex_data(query, output_file):
    """ Fetch data from OpenAlex API and save as JSON """
    url = f"https://api.openalex.org/works?filter=concepts.id:{query}&per-page=100"

    # If an API key is available, append it to the request
    if OPENALEX_API_KEY:
        url += f"&api_key={OPENALEX_API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        with open(os.path.join(RAW_DATA_PATH, output_file), "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {output_file}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    # Example: Fetch data for AI (OpenAlex Concept ID: C277839011)
    fetch_openalex_data("C277839011", "ai_data.json")
