import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAW_DATA_PATH = "data-extraction/raw_data/"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

OPENALEX_API_KEY = os.getenv("OPENALEX_API_KEY")

def fetch_openalex_data(concept_id, start_year, end_year, output_file):
    """
    Fetch publication data for a given concept ID and year range from OpenAlex API
    """
    url = f"https://api.openalex.org/works?filter=concepts.id:{concept_id},publication_year:{start_year}|{end_year}&per-page=100"

    # Append API key if available
    if OPENALEX_API_KEY:
        url += f"&api_key={OPENALEX_API_KEY}"
    
    response = requests.get(url)
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        output_path = os.path.join(RAW_DATA_PATH, output_file)
        with open(output_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {output_file}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(f"Response Content: {response.content}")

if __name__ == "__main__":
    # Fetch data for Artificial Intelligence (C154945302) from 2010 to 2020
    fetch_openalex_data("C154945302", 2010, 2020, "ai_2010_2020.json")
