import requests
import json
import csv
import os
from time import sleep

# Constants
RAW_DATA_DIR = "data-extraction/raw_data"
OUTPUT_CSV = "data-analysis/vosviewer_data.csv"
CONCEPT_IDS = {
    "AI": "C154945302",
    "Deep Learning": "C108583219"
}
YEARS = list(range(2010, 2021))
PER_PAGE = 200
MAX_PAGES = 5  # adjust based on your quota and need

# Ensure folders exist
os.makedirs("data-analysis", exist_ok=True)


def fetch_works(concept_id, year):
    all_results = []
    for page in range(1, MAX_PAGES + 1):
        url = f"https://api.openalex.org/works?filter=concepts.id:{concept_id},publication_year:{year}&per-page={PER_PAGE}&page={page}"
        print(f"Fetching: {url}")
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Failed on page {page}: {res.status_code}")
            break

        data = res.json()
        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)
        sleep(1)  # Be polite to API
    return all_results


def extract_csv_data(raw_data, field_label):
    rows = []
    for item in raw_data:
        title = item.get("title", "N/A")
        pub_year = item.get("publication_year", "")
        citation_count = item.get("cited_by_count", 0)
        authorships = item.get("authorships", [])
        countries = []
        for auth in authorships:
            inst = auth.get("institutions", [])
            for i in inst:
                country = i.get("country_code")
                if country:
                    countries.append(country)

        countries = ", ".join(set(countries)) or "Unknown"

        rows.append([
            field_label,
            title,
            pub_year,
            citation_count,
            countries
        ])
    return rows


def main():
    all_rows = []
    for label, concept_id in CONCEPT_IDS.items():
        for year in YEARS:
            raw = fetch_works(concept_id, year)
            print(f"Year {year} | {label} | {len(raw)} records")
            extracted = extract_csv_data(raw, label)
            all_rows.extend(extracted)

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Field", "Title", "Year", "Cited By Count", "Countries"])
        writer.writerows(all_rows)

    print(f"✅ Data saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
